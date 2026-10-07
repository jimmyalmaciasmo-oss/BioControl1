import os
import sys
from github import Github, GithubException

class GitHubAssistant:
    def __init__(self, token: str = None):
        """
        Inicializa el asistente virtual.
        Intenta leer el token desde la variable de entorno GITHUB_TOKEN o se pasa directamente.
        """
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.gh = None
        self.user = None
        self.name = "GitBot"
        
        if self.token:
            self._connect()
        else:
            print("⚠️ Aviso: No se detectó un GITHUB_TOKEN. Algunas funciones estarán limitadas.")

    def _connect(self):
        try:
            self.gh = Github(self.token)
            self.user = self.gh.get_user()
            print(f" Conectado exitosamente como: {self.user.login}")
        except GithubException as e:
            print(f"❌ Error al conectar con la API de GitHub: {e.status} - {e.data.get('message', '')}")
            self.gh = None

    def get_user_profile((self) -> str:
        if not self.user:
            return "No estás autenticado en GitHub."
        return f"👤 Usuario: {self.user.login} | Repositorios Públicos: {self.user.public_repos} | Seguidores: {self.user.followers}"

    def list_repositories(self, limit: int = 5) -> str:
        if not self.user:
            return "Necesitas un token de GitHub válido para ver tus repositorios."
        try:
            repos = [repo.name for repo in self.user.get_repos()[:limit]]
            if not repos:
                return "No se encontraron repositorios."
            return f"📂 Tus últimos {len(repos)} repositorios:\n - " + "\n - ".join(repos)
        except Exception as e:
            return f"Error al obtener repositorios: {str(e)}"

    def get_commit_info(self, repo_name: str, commit_sha: str) -> str:
        """Obtiene detalles de un commit específico."""
        try:
            gh_client = self.gh if self.gh else Github()
            repo = gh_client.get_repo(repo_name)
            commit = repo.get_commit(sha=commit_sha)
            
            author = commit.commit.author.name
            date = commit.commit.author.date.strftime("%Y-%m-%d %H:%M:%S")
            message = commit.commit.message.strip()
            files_count = len(commit.files)
            
            return (
                f"📝 Commit: {commit_sha[:7]}\n"
                f"👤 Autor: {author}\n"
                f"📅 Fecha: {date}\n"
                f"💬 Mensaje: {message}\n"
                f"📁 Archivos modificados: {files_count}"
            )
        except Exception as e:
            return f"❌ Error al consultar el commit: {str(e)}"

    def process_request(self, text: str) -> str:
        command = text.strip().lower()

        if command in ["perfil", "profile", "quien soy"]:
            return self.get_user_profile()
        elif command in ["repos", "repositorios", "mis repos"]:
            return self.list_repositories()
        elif command.startswith("commit "):
            # Formato esperado: commit usuario/repo hash
            parts = text.split()
            if len(parts) >= 3:
                return self.get_commit_info(parts[1], parts[2])
            return "Uso correcto: `commit usuario/repositorio HASH`"
        elif command in ["ayuda", "help"]:
            return (
                "Comandos disponibles:\n"
                "- `perfil`: Muestra la información de tu cuenta.\n"
                "- `repos`: Lista tus repositorios recientes.\n"
                "- `commit <usuario/repo> <hash>`: Consulta detalles de un commit.\n"
                "- `salir`: Cierra la sesión."
            )
        else:
            return f"Comando no reconocido. Escribe 'ayuda' para ver las opciones disponibles."

    def start(self):
        print(f"=== {self.name} activado ===")
        print("Escribe 'ayuda' para ver la lista de comandos o 'salir' para terminar.\n")

        while True:
            try:
                user_input = input("Tú: ").strip()
                if not user_input:
                    continue

                if user_input.lower() in ["salir", "exit", "quit"]:
                    print(f"\n{self.name}: ¡Hasta luego!")
                    break

                response = self.process_request(user_input)
                print(f"\n{self.name}:\n{response}\n")

            except (KeyboardInterrupt, EOFError):
                print(f"\n\n{self.name}: Sesión finalizada.")
                break

if __name__ == "__main__":
    # Si deseas hardcodear el token para pruebas locales, colócalo aquí.
    # Recomendado: Usa la variable de entorno GITHUB_TOKEN en lugar de pegar tokens en el código.
    TOKEN = None 

    assistant = GitHubAssistant(token=TOKEN)
    assistant.start()
