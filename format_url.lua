#!lua
-- Lua script to convert a URL path in the clipboard to a standard file path

-- Function to decode URL-encoded characters
function url_decode(url)
    url = url:gsub("%%(%x%x)", function(hex)
        return string.char(tonumber(hex, 16))
    end)
    return url
end

-- Retrieve the clipboard content using xclip or xsel
local handle = io.popen("xclip -selection clipboard -o 2>/dev/null || xsel --clipboard --output 2>/dev/null")
local url_path = handle:read("*a")
handle:close()

-- Check if clipboard retrieval was successful
if url_path and url_path ~= "" then
    local decoded_path = url_decode(url_path):gsub("file://", "") -- Remove 'file://' prefix if present
    print('"'..decoded_path..'"')
else
    print("Error: Could not retrieve clipboard content or clipboard is empty.")
end
