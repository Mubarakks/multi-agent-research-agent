from agents import search_agent,reader_agent,writer_chain,critic_chain
from langchain_core.messages import HumanMessage
def Base_research_pipeline(topic:str)-> dict:

    state={}
    
    print('\n'+'='*50)
    print('step 1 - search agent is working ....')
    print('='*50)

    searcher_agent=search_agent()
    search_result = searcher_agent.invoke({
        'messages':[('user',f'find recent, reliable and detailed information about :{topic}')]
    })

    state['search_results']=search_result['messages'][-1].content

    print ('\n search results',state['search_results'])

    # reader agent
    print('\n'+'='*50)
    print('step 1 - reader agent is working on scraping resources ....')
    print('='*50)


    readers_agent = reader_agent()
    reader_results = readers_agent.invoke({
        "messages":[HumanMessage (content=
                f"""based on following search results about '{topic}',
                ick the most relevant URL and scrape it for deeper content.'

                Search Results:{state['search_results']}
                """
            )
        ]
    })

    state['scraped_content'] = reader_results['messages'][-1].content

    print('scraped content', state['scraped_content'])

    # writer chain
    print('\n'+'='*50)
    print('step 1 - writer is working on report ....')
    print('='*50)

    combined_research = (
    f"Search Results:\n{state['search_results']}\n\n"
    f"Detailed scraped content:\n{state['scraped_content']}"
    )
    state['report']=writer_chain.invoke({
        'topic':topic,
        'research':combined_research
    })

    print('\n final report\n',state['report'])

    # critic report

    print('\n'+'='*50)
    print('step 1 - critic working on report ....')
    print('='*50)

    state['feedback']=critic_chain.invoke({
        'report':state['report']
    })

    print('\n critic report \n', state['feedback'])

    return state


if __name__ =='__main__':
    topic = input('\n enter a research topic ')
    Base_research_pipeline(topic)