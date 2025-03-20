tell application "Terminal"
	activate
	do script "cd /Users/danawunderlich/CascadeProjects/squaring_new && ./start_squaring_app.sh"
end tell

-- Wait for server to start
delay 3

-- Open in default browser
do shell script "open http://localhost:5015"
