import csv
import feedparser
import re

def extract_job_details(description):
    skills_match = re.search(r'Skills required:<br />(.*?)<br /><br />', description, re.DOTALL)
    skills_required = skills_match.group(1).strip() if skills_match else None

    job_details_match = re.search(r'<b>Posted On<\/b>:(.*?)<br /><b>Category<\/b>:(.*?)<br /><b>Skills<\/b>:(.*?)<br /><b>Country<\/b>:(.*?)<br /><a href="(.*?)">', description, re.DOTALL)
    posted_on, category, skills, country, apply_link = job_details_match.groups() if job_details_match else (None, None, None, None, None)

    return {
        'Skills Required': skills_required,
        'Posted On': posted_on.strip() if posted_on else None,
        'Category': category.strip() if category else None,
        'Skills': skills.strip() if skills else None,
        'Country': country.strip() if country else None,
        'Apply Link': apply_link.strip() if apply_link else None,
    }

def fetch_upwork_jobs_rss(feed_url):
    feed = feedparser.parse(feed_url)

    if 'entries' in feed:
        with open('upwork_jobs.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Link', 'Published Date', 'Description', 'Skills Required', 'Posted On', 'Category', 'Skills', 'Country', 'Apply Link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for entry in feed.entries:
                job_details = extract_job_details(entry.description)
                writer.writerow({
                    'Title': entry.title,
                    'Link': entry.link,
                    'Published Date': entry.published,
                    'Description': entry.description,
                    'Skills Required': job_details['Skills Required'],
                    'Posted On': job_details['Posted On'],
                    'Category': job_details['Category'],
                    'Skills': job_details['Skills'],
                    'Country': job_details['Country'],
                    'Apply Link': job_details['Apply Link'],
                })

if __name__ == "__main__":
    upwork_rss_url = "https://www.upwork.com/ab/feed/jobs/rss?paging=10%3B10&sort=recency&api_params=1&q=&securityToken=a3d75c4275bd54a3509cd27e00e5c00658c0c463ea831adeff073b687509fadb58175b09dc4a8ad7e438b70d8540d8e4a40e5063ba1a95497fd4dfb38c13db50&userUid=997168601881923584&orgUid=1718343678507720704"
    fetch_upwork_jobs_rss(upwork_rss_url)
