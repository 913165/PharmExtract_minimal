# Example endpoint to add to main.py for viewing logs
# Only add this if you need remote log access

@app.route("/logs/recent")
def view_recent_logs():
    """View recent log entries (protected endpoint)."""
    # Check for authentication
    auth_token = request.args.get('token') or request.headers.get('X-Log-Token')
    expected_token = os.environ.get('LOG_ACCESS_TOKEN')
    
    if not expected_token or auth_token != expected_token:
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        # Check if persistent storage exists
        if not os.path.exists("/data/logs"):
            return jsonify({"error": "No persistent storage available"}), 404
        
        # Get today's log file
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = f"/data/logs/radextract-{today}.log"
        
        if not os.path.exists(log_file):
            return jsonify({"error": "No logs for today"}), 404
        
        # Read last 100 lines
        with open(log_file, 'r') as f:
            lines = f.readlines()
            recent_lines = lines[-100:] if len(lines) > 100 else lines
        
        # Filter for request logs
        request_logs = [
            line.strip() for line in recent_lines 
            if "[Req " in line and ("🔴" in line or "🟢" in line)
        ]
        
        return jsonify({
            "log_file": log_file,
            "total_lines": len(lines),
            "recent_requests": request_logs
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500 