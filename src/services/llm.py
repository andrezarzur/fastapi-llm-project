from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from src.domains.properties.schemas import PropertyBase as PropertySchema
from src.config.setting import Settings
from fastapi import HTTPException


def get_property_description(property: PropertySchema):
    try:
        template = """Question: {question}
    
        Answer: General one sentence attractive sentence, don't mention being provided metadata."""
        prompt = ChatPromptTemplate.from_template(template)
        model = OllamaLLM(model=Settings().LLM_MODEL)
        chain = prompt | model
        result = chain.invoke({"question": "Give me a description for this property based on it's metadata: type -> "
                                           + property.property_type + " price -> " + str(property.price) + " area -> " +
                                           str(property.area) + " bedrooms -> " + str(property.bedrooms) + " bathrooms -> "
                                           + str(property.bathrooms) + " parking -> " + str(property.parking)
                               })

        return result
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"An error occurred: {err}")
