# docker build -t demo_kowabunga .

FROM continuumio/miniconda3

WORKDIR /home/app

COPY requirements.txt /dependencies/requirements.txt
RUN pip install -r /dependencies/requirements.txt

# on ne fait pas de partage de répertoire
# on ne copie que le fichier app.py
copy app.py .  

# sur la machine linux on lancerait à la main l'application avec "streamlit run app.py" 
CMD ["streamlit", "run", "app.py"]

