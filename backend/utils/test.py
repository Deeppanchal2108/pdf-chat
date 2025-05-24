from langchain_cohere import ChatCohere
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

template =PromptTemplate(template="Capital of this country is {country}?", input_variables=["country"])

model = ChatCohere()
prompt=template.invoke({"country":"india"})
result = model.invoke(prompt)
print(result)