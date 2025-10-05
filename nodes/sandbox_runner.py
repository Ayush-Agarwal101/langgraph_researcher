# FILE: nodes/sandbox_runner.py

import docker
import os
import uuid
import json
from typing import Dict, Any

def sandbox_runner_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("---NODE: SANDBOX RUNNER---")
    code = state.get("code")
    dockerfile = state.get("dockerfile")
    
    run_id = str(uuid.uuid4())
    workspace_path = os.path.join("sandbox", run_id)
    os.makedirs(workspace_path, exist_ok=True)
    print(f"📦 Created temporary workspace: {workspace_path}")

    results = {}
    try:
        with open(os.path.join(workspace_path, "experiment.py"), "w") as f:
            f.write(code)
        with open(os.path.join(workspace_path, "Dockerfile"), "w") as f:
            f.write(dockerfile)

        client = docker.from_env()
        image_tag = f"research-run-{run_id}"
        print(f"🐳 Building Docker image: {image_tag}")
        image, _ = client.images.build(path=workspace_path, tag=image_tag, rm=True)
        print("✅ Docker image built.")

        print(f"🚀 Running container...")
        container = client.containers.run(image_tag, detach=False, remove=True)
        print("✅ Container finished.")

        results_path = os.path.join(workspace_path, "results.json")
        if os.path.exists(results_path):
            with open(results_path, "r") as f:
                results = json.load(f)
            print("📊 Results retrieved:")
            print(json.dumps(results, indent=2))
        else:
            print("⚠️ No results.json file found.")
            results = {"error": "results.json not found"}

    except Exception as e:
        print(f"❌ An error occurred in the sandbox: {e}")
        results = {"error": str(e)}
        
    return {"results": results}