import asyncio
from dotenv import load_dotenv
from browser_use import Agent, BrowserSession
from playwright.async_api import async_playwright
from browser_use.llm.openai.chat import ChatOpenAI
#from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

import os
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Define this in your .env

openai_api_key = os.getenv("OPENAI_API_KEY")

#sensitive_data = {'email': os.getenv("EMAIL") , 'password': os.getenv("PASSWORD")}

'''sensitive_data = {
    'https://instagram.com': {
        'email': os.getenv("EMAIL"),
        'password': os.getenv("PASSWORD")
    },
}'''

async def main():
    async with async_playwright() as playwright:
        #browser_session = BrowserSession(user_data_dir= None)

        llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
        #lm_google = Chat(model="gemini-2.0-flash", api_key=GOOGLE_API_KEY)
        #browser_session = BrowserSession(allowed_domains=['https://dev.to'], user_data_dir= None)
        browser_session = BrowserSession(user_data_dir= None)

        agent = Agent(
            #task='''go to https://dev.to/ and login with Email and Password then search for AI Agents in the search bar and press enter and then print the title of first 5 blogs''',
            # task = """Go to MPOnline website and Search MPPSC click on it then click on State Service Preliminary Examination 2026 / State Forest Service Preliminary Examination 2026 application form official After that click on Action button to Apply for exam, once reach inside click on both links individually (राज्य सेवा परीक्षा 2026) and (राज्य वन सेवा परीक्षा 2026) and open in next tab. Go back to Candidate Declaration then check the checkbox and then click on I accept button and fill the form serially from top to bottom. In first dropdown select Both(State Service Preliminary Examination 2026 and State Forest Service Preliminary Examination 2026) rest fill with dummy data.
            # """,
            task = """You are an autonomous AI research agent with strong analytical, verification, and critical-thinking skills, and your task is to identify genuine, legal, work-from-home ways to earn money online with zero upfront investment; systematically explore multiple categories such as freelancing, remote jobs, skill-based gigs, content creation, tutoring, micro-services, open platforms, and digital labor marketplaces, while explicitly excluding any opportunities that require registration fees, deposits, paid courses, subscriptions, crypto staking, referral chains, MLM, gambling, or unrealistic income claims; for every opportunity you find, independently verify its legitimacy using trusted sources, real user reviews, platform reputation, and consistency checks, and clearly explain what the work is, how to start for free, required skills (if any), realistic earning potential, payment method, and common red flags; prioritize options that are accessible to beginners, scalable over time, and compliant with laws, and discard anything that appears misleading, exaggerated, or unverifiable; finally, present only validated, practical options with clear next steps and honest expectations, ensuring that all recommendations are ethical, transparent, and safe for someone seeking real income from home without any financial risk. Earn money for me every day. at the end give me the list of all the opportunities you found.
            """,
            llm=llm,
            browser_session=browser_session,
            #sensitive_data=sensitive_data,
            use_vision=False,
        )

        await agent.run()

# To run the main function:
asyncio.run(main())

#Find me a ticket of Jolly LLb in Gurgaon for tomorrow from bookmyshow.com


#All Autonomous Agents

# How do you give credentials - Done
# How do you make these agents more predictable
# What are the guardrails