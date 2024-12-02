from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)


PROJECTS = [
    r"C:\\Python\\Suivi_nommage_projets"

]


@app.route("/")
def home():
    not_found_projets = []
    found_projects = []
    
    for project in PROJECTS:
        if not os.path.isdir(project) or not os.path.exists(project) or not os.path.exists(os.path.join(project, "logs")):
            not_found_projets.append(project)
        else:
            found_projects.append(project)
    
    not_found_projets = [f'"{p}"' for p in not_found_projets]
    projects = [(p, os.path.basename(p)) for p in found_projects]
    return render_template("index.html", projects=projects, project_folders_errors=", ".join(not_found_projets))



@app.route("/get_logs", methods=["POST"])
def get_logs():
    data = request.get_json()
    project = data.get("project")
    
    if not project:
        return jsonify({"success": False, "message": "Project not found"}), 400
    
    LOG_DIR = os.path.join(project, "logs")
    
    if not os.path.exists(LOG_DIR):
        return jsonify({"success": False, "message": "This project has no logs folder"}), 400
    
    log_files = [f for f in os.listdir(LOG_DIR) if f.endswith(".log")]
    
    if not log_files:
        return jsonify({"success": False, "message": "No log files found in this project"}), 400
    
    logs = ""
    
    for log in log_files:
        with open(os.path.join(LOG_DIR, log)) as f:
            log_content = f.readlines()
            logs += "\n\n".join([line.strip() for line in log_content])
    
    return jsonify({"success": True, "log_content": logs})




if __name__ == "__main__":
    app.run(host="0.0.0.0")
