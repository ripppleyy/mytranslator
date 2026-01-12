string API_URL = "https://mytranslator-45dr.onrender.com/translate";
integer translate_enabled = TRUE; // starts ON

default
{
    state_entry()
    {
        llListen(0, "", NULL_KEY, "");
        // Initial indicator
        if (translate_enabled)
        {
            llSetText("Translator: ON", <0.0, 1.0, 0.0>, 1.0); // green
        }
        else
        {
            llSetText("Translator: OFF", <1.0, 0.0, 0.0>, 1.0); // red
        }
        llOwnerSay("Translator active. Use !trans on/off to toggle (group only).");
    }

    listen(integer channel, string name, key id, string msg)
    {
        string lower = llToLower(msg);

        // --- GROUP CHECK FOR TOGGLE COMMANDS ---
        if (lower == "!trans on" || lower == "!trans off")
        {
            if (!llSameGroup(id))
            {
                llRegionSayTo(id, 0, "You must be in the same group as this device to control it.");
                return;
            }

            if (lower == "!trans on")
            {
                translate_enabled = TRUE;
                llOwnerSay("Translation enabled.");
                llSetText("Translator: ON", <0.0, 1.0, 0.0>, 1.0); // green
                return;
            }

            if (lower == "!trans off")
            {
                translate_enabled = FALSE;
                llOwnerSay("Translation disabled.");
                llSetText("Translator: OFF", <1.0, 0.0, 0.0>, 1.0); // red
                return;
            }
        }

        // If translation is off, ignore everything else
        if (!translate_enabled) return;

        // Ignore the object's own messages
        if (id == llGetKey()) return;

        // Build JSON body
        string body = llList2Json(JSON_OBJECT, [
            "q", msg,
            "target", "en"
        ]);

        llHTTPRequest(
            API_URL,
            [
                HTTP_METHOD, "POST",
                HTTP_MIMETYPE, "application/json"
            ],
            body
        );
    }

    http_response(key req, integer status, list meta, string body)
    {
        if (status != 200)
        {
            llOwnerSay("HTTP error: " + (string)status);
            return;
        }

        string translated = llJsonGetValue(body, ["translatedText"]);
        string detected = llJsonGetValue(body, ["detectedSourceLanguage"]);

        // BLOCK English → English
        if (detected == "en")
        {
            return;
        }

        llSay(0, "[EN] " + translated);
    }
}
