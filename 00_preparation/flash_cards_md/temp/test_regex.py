import re
from pathlib import Path

k_QAFolder = "../static/md"  # relative to "this" python source file


# TODO : penser aux cas où on va avoir plusieurs fichiers md avec des questions et des réponses
def parse_markdown(qa_pairs, markdown_text):

    pattern = re.compile(r"\* Question : (.*?)\* Réponse\s*: (.*?)(?=\n\* Question|\Z)", re.DOTALL)
    matches = pattern.findall(markdown_text)

    for match in matches:
        question, answer = match
        qa_pairs.append({"question": question.strip(), "answer": answer.strip()})

    return qa_pairs


p = Path(__file__).parent
qaFolder = p / k_QAFolder


list_qa_files = [item for item in qaFolder.iterdir() if item.is_file()]
qa_pairs = []
for qa_file in list_qa_files:
    try:
        with qa_file.open("r", encoding="utf-8") as f:
            markdown_text = f.read()
            qa_pairs = parse_markdown(qa_pairs, markdown_text)
    except Exception as e:
        print(f"Error reading file {file.name}: {e}")
print(qa_pairs)
