import httpx , json , os
from dotenv import load_dotenv

load_dotenv()

async def ai_analyze(prompt):
    async with httpx.AsyncClient() as client:
        response=await client.post(
            url=os.getenv('OPENROUTER_URL'),
            headers={
                "Authorization": os.getenv('TOKEN_OPENROUTER'),
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": os.getenv('OPENROUTER_MODEL'),
                "messages": [
                    {
                    "role": "user",
                    "content": prompt
                    }
                ],
                "reasoning": {"enabled": True}
            }) 
        )
        response.raise_for_status()
        response_py=response.json()
        ai_response=response_py['choices'][0]['message']
        return ai_response


