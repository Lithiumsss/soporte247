import os
import time
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}
OWNER = "Lithiumsss"

# Lista de tus repositorios configurados con la clase correcta
REPOS = [
    "LITHIUMS1",
    "LITHIUMS2",
    "LITHIUMS3",
    "LITHIUMS4",
    "LITHIUMS5",
    "LITHIUMS6",
    "LITHIUMS7",
    "LITHIUMS8",
    "LITHIUMS9",
    "LITHIUMS10",
    "LITHIUMS11",
    "LITHIUMS12",
    "LITHIUMS13",
    "LITHIUMS14",
    "LITHIUMS15",
    "LITHIUMS16",
    "LITHIUMS17",
    "LITHIUMS18",
    "LITHIUMS19"
]
WORKFLOW_FILE = "run.yml"

def verificar_estado_proyecto(repo_name):
    url = f"https://api.github.com/repos/{OWNER}/{repo_name}/actions/workflows/{WORKFLOW_FILE}/runs?per_page=1"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            runs = response.json().get("workflow_runs", [])
            if runs:
                estado_actual = runs[0].get("status")
                conclusion = runs[0].get("conclusion")
                return estado_actual, conclusion
    except Exception as e:
        print(f"Error al verificar {repo_name}: {e}")
    return None, None

def trigger_workflow(repo_name):
    url = f"https://api.github.com/repos/{OWNER}/{repo_name}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    payload = {"ref": "main"}
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        if response.status_code == 204:
            print(f"Workflow relanzado con éxito para: {repo_name}")
        else:
            print(f"Error al relanzar {repo_name}: {response.text}")
    except Exception as e:
        print(f"Error al disparar workflow en {repo_name}: {e}")

if __name__ == "__main__":
    print("Iniciando supervisor 24/7 inteligente...")
    
    while True:
        for repo in REPOS:
            print(f"Revisando repositorio: {repo}...")
            status, conclusion = verificar_estado_proyecto(repo)
            
            # Si el proyecto ya terminó (completado), el supervisor lo relanza automáticamente
            if status == "completed":
                print(f"El proyecto {repo} ha terminado (conclusion: {conclusion}). Relanzando...")
                trigger_workflow(repo)
            elif status == "in_progress":
                print(f"El proyecto {repo} sigue en curso. Esperando...")
            else:
                print(f"El proyecto {repo} no tiene ejecuciones activas o está en espera.")
                
        # Pausa de 60 segundos antes del siguiente ciclo de revisión
        time.sleep(60)
