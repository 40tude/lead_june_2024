# Pour faire le test en local
# Il faut que l'image demo_kowabunga soit disponible => docker build -t demo_kowabunga .
# Faudra pointer le browser sur https://localhost:4000

docker run -it --rm `
-p 4000:8501 `
demo_kowabunga `
