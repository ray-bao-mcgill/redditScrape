import requests
from bs4 import BeautifulSoup
import re
import time

def get_top_universities():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Complete mapping of subreddits to university names
    university_map = {
        'uoft': 'University of Toronto',
        'UBC': 'University of British Columbia',
        'mcgill': 'McGill University',
        'uAlberta': 'University of Alberta',
        'uwaterloo': 'University of Waterloo',
        'queensuniversity': "Queen's University",
        'UCalgary': 'University of Calgary',
        'uottawa': 'University of Ottawa',
        'uwo': 'Western University',
        'dalhousie': 'Dalhousie University',
        'uofm': 'University of Manitoba',
        'uvic': 'University of Victoria',
        'yorku': 'York University',
        'simonfraser': 'Simon Fraser University',
        'Concordia': 'Concordia University',
        'uSask': 'University of Saskatchewan',
        'CarletonU': 'Carleton University',
        'udem': 'Université de Montréal',
        'ulaval': 'Université Laval',
        'WilfridLaurier': 'Wilfrid Laurier University',
        'uoguelph': 'University of Guelph',
        'uwindsor': 'University of Windsor',
        'brocku': 'Brock University',
        'ryerson': 'Ryerson University (Toronto Metropolitan University)',
        'TrentUniversity': 'Trent University',
        'MemorialUniversity': 'Memorial University of Newfoundland',
        'UQAM': 'Université du Québec à Montréal',
        'SaintMarys': "Saint Mary's University",
        'UNB': 'University of New Brunswick',
        'Sherbrooke': 'Université de Sherbrooke',
        'ASU': 'Arizona State University',
        'ucla': 'University of California, Los Angeles',
        'berkeley': 'University of California, Berkeley',
        'Harvard': 'Harvard University',
        'stanford': 'Stanford University',
        'mit': 'Massachusetts Institute of Technology',
        'uofm': 'University of Michigan',
        'USC': 'University of Southern California',
        'uchicago': 'University of Chicago',
        'nyu': 'New York University',
        'ufl': 'University of Florida',
        'UTAustin': 'University of Texas at Austin',
        'udub': 'University of Washington',
        'OSU': 'Ohio State University',
        'UNC': 'University of North Carolina at Chapel Hill',
        'UIUC': 'University of Illinois at Urbana-Champaign',
        'PennStateUniversity': 'Pennsylvania State University',
        'duke': 'Duke University',
        'Cornell': 'Cornell University',
        'princeton': 'Princeton University',
        'yale': 'Yale University',
        'UVA': 'University of Virginia',
        'UWMadison': 'University of Wisconsin-Madison',
        'BostonU': 'Boston University',
        'Purdue': 'Purdue University',
        'Northwestern': 'Northwestern University',
        'uofmn': 'University of Minnesota',
        'aggies': 'Texas A&M University',
        'UMD': 'University of Maryland',
        'Pitt': 'University of Pittsburgh',
        'IndianaUniversity': 'Indiana University Bloomington',
        'UCSD': 'University of California, San Diego',
        'UGA': 'University of Georgia',
        'UCDavis': 'University of California, Davis',
        'cmu': 'Carnegie Mellon University',
        'umiami': 'University of Miami',
        'FSU': 'Florida State University',
        'cuboulder': 'University of Colorado Boulder',
        'UofArizona': 'University of Arizona',
        'uiowa': 'University of Iowa',
        'UCONN': 'University of Connecticut',
        'udel': 'University of Delaware',
        'UniversityofKansas': 'University of Kansas',
        'uky': 'University of Kentucky',
        'UNLincoln': 'University of Nebraska-Lincoln',
        'mizzou': 'University of Missouri',
        'rutgers': 'Rutgers University',
        'ucf': 'University of Central Florida',
        'UNLV': 'University of Nevada, Las Vegas',
        'VirginiaTech': 'Virginia Tech',
        'Clemson': 'Clemson University',
        'Auburn': 'Auburn University',
        'georgetown': 'Georgetown University',
        'NEU': 'Northeastern University',
        'Temple': 'Temple University',
        'SDSU': 'San Diego State University',
        'SJSU': 'San Jose State University',
        'SMU': 'Southern Methodist University',
        'depaul': 'DePaul University',
        'Marquette': 'Marquette University',
        'gmu': 'George Mason University',
        'AmericanU': 'American University',
        'UTK': 'University of Tennessee',
        'Gamecocks': 'University of South Carolina',
        'unt': 'University of North Texas',
        'LSU': 'Louisiana State University',
        'olemiss': 'University of Mississippi',
        'MSU': 'Montana State University',
        'uvm': 'University of Vermont'
    }
    
    subreddits = []
    
    for subreddit, university in university_map.items():
        try:
            url = f"https://old.reddit.com/r/{subreddit}"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            subscribers_div = soup.find('span', {'class': 'number'})
            if subscribers_div:
                subscriber_text = subscribers_div.text
                subscribers = int(re.sub(r'[^\d]', '', subscriber_text))
                
                subreddits.append({
                    'university': university,
                    'subreddit': subreddit,
                    'subscribers': subscribers
                })
                print(f"Processed {university} (r/{subreddit}) - {subscribers:,} subscribers")
            
            time.sleep(2)
            
        except Exception as e:
            print(f"Error processing {university} (r/{subreddit}): {e}")
            continue
    
    # Sort by subscriber count
    subreddits.sort(key=lambda x: x['subscribers'], reverse=True)
    
    # Find U of T's index (changed to lowercase 'uoft')
    uoft_index = next(i for i, s in enumerate(subreddits) if s['subreddit'].lower() == 'uoft')
    
    # Return U of T and the next 29 universities
    return subreddits[uoft_index:uoft_index + 30]

if __name__ == "__main__":
    print("Fetching subscriber counts for university subreddits...")
    top_unis = get_top_universities()
    
    print("\nU of T and Next 29 Universities by Subreddit Subscriber Count:")
    print("-" * 70)
    for idx, uni in enumerate(top_unis, 1):
        print(f"{idx}. {uni['university']}: r/{uni['subreddit']} - {uni['subscribers']:,} subscribers")
