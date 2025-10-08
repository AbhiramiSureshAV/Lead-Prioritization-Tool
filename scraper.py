import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import urljoin, urlparse
import pandas as pd

# Rate limiting and ethical scraping
REQUEST_DELAY = 1.0  # seconds between requests
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

def get_session():
    """Create a session with proper headers for ethical scraping"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    })
    return session

def rate_limit():
    """Simple rate limiting to respect servers"""
    time.sleep(REQUEST_DELAY)

def extract_domain_from_company(company_name):
    """Extract potential domain from company name"""
    # Simple heuristic: company name -> company.com
    clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', company_name.lower())
    clean_name = re.sub(r'\s+', '', clean_name)
    return f"{clean_name}.com"

def search_company_info(company_name, domain=None):
    """Search for company information using Google and other sources"""
    session = get_session()
    
    if not domain:
        domain = extract_domain_from_company(company_name)
    
    # Simulate data enrichment (in production, you'd use real APIs)
    # This is a mock implementation for the prototype
    
    company_data = {
        'company_name': company_name,
        'domain': domain,
        'email': '',
        'phone': '',
        'linkedin': '',
        'industry': '',
        'location': '',
        'company_size': '',
        'revenue_range': '',
        'growth_signals': '',
        'description': ''
    }
    
    try:
        # Simulate web scraping with rate limiting
        rate_limit()
        
        # Mock industry detection based on company name patterns
        industry = detect_industry(company_name)
        company_data['industry'] = industry
        
        # Mock revenue estimation
        revenue_range = estimate_revenue(company_name, industry)
        company_data['revenue_range'] = revenue_range
        
        # Mock contact information generation
        company_data['email'] = generate_contact_email(company_name, domain)
        company_data['phone'] = generate_phone_number()
        company_data['linkedin'] = generate_linkedin_url(company_name)
        
        # Mock location and company size
        company_data['location'] = generate_location()
        company_data['company_size'] = generate_company_size()
        
        # Mock growth signals
        company_data['growth_signals'] = detect_growth_signals(company_name, industry)
        
        # Mock description
        company_data['description'] = generate_company_description(company_name, industry)
        
    except Exception as e:
        # Return basic data even if enrichment fails
        company_data['industry'] = 'Unknown'
        company_data['revenue_range'] = 'Unknown'
    
    return company_data

def detect_industry(company_name):
    """Detect industry based on company name patterns"""
    name_lower = company_name.lower()
    
    # SaaS/Tech keywords
    saas_keywords = ['software', 'tech', 'cloud', 'saas', 'platform', 'api', 'digital', 'data', 'ai', 'ml', 'automation']
    if any(keyword in name_lower for keyword in saas_keywords):
        return 'SaaS/Tech'
    
    # Healthcare keywords
    health_keywords = ['health', 'medical', 'pharma', 'biotech', 'wellness', 'care', 'clinical']
    if any(keyword in name_lower for keyword in health_keywords):
        return 'Healthcare'
    
    # Finance keywords
    finance_keywords = ['finance', 'fintech', 'bank', 'payment', 'trading', 'investment', 'crypto']
    if any(keyword in name_lower for keyword in finance_keywords):
        return 'Financial Services'
    
    # E-commerce keywords
    ecommerce_keywords = ['retail', 'commerce', 'marketplace', 'shop', 'store', 'ecommerce']
    if any(keyword in name_lower for keyword in ecommerce_keywords):
        return 'E-commerce'
    
    # Manufacturing keywords
    manufacturing_keywords = ['manufacturing', 'industrial', 'factory', 'production', 'supply']
    if any(keyword in name_lower for keyword in manufacturing_keywords):
        return 'Manufacturing'
    
    return 'Other'

def estimate_revenue(company_name, industry):
    """Estimate revenue range based on company characteristics"""
    name_lower = company_name.lower()
    
    # High-revenue indicators
    high_revenue_indicators = ['enterprise', 'corporate', 'global', 'international', 'systems', 'solutions']
    if any(indicator in name_lower for indicator in high_revenue_indicators):
        return 'High ($1M+)'
    
    # Industry-based estimation
    if industry in ['SaaS/Tech', 'Financial Services']:
        # Higher likelihood of high revenue for these industries
        return random.choices(['Medium ($100K-$1M)', 'High ($1M+)'], weights=[40, 60])[0]
    elif industry in ['Healthcare', 'Manufacturing']:
        return random.choices(['Low (<$100K)', 'Medium ($100K-$1M)', 'High ($1M+)'], weights=[20, 50, 30])[0]
    else:
        return random.choices(['Low (<$100K)', 'Medium ($100K-$1M)', 'High ($1M+)'], weights=[30, 50, 20])[0]

def generate_contact_email(company_name, domain):
    """Generate realistic contact email addresses"""
    if not domain or domain == 'unknown.com':
        return ''
    
    # Common email patterns
    email_patterns = [
        'info@{}',
        'contact@{}',
        'hello@{}',
        'sales@{}',
        'support@{}'
    ]
    
    pattern = random.choice(email_patterns)
    return pattern.format(domain)

def generate_phone_number():
    """Generate realistic phone numbers"""
    # US phone number format
    area_codes = ['212', '415', '650', '312', '617', '310', '206', '503', '713', '305']
    area_code = random.choice(area_codes)
    number = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return f"({area_code}) {number[:3]}-{number[3:]}"

def generate_linkedin_url(company_name):
    """Generate LinkedIn company page URL"""
    clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', company_name.lower())
    clean_name = re.sub(r'\s+', '-', clean_name)
    return f"https://linkedin.com/company/{clean_name}"

def generate_location():
    """Generate realistic company locations"""
    locations = [
        'San Francisco, CA', 'New York, NY', 'Austin, TX', 'Seattle, WA',
        'Boston, MA', 'Chicago, IL', 'Denver, CO', 'Portland, OR',
        'Los Angeles, CA', 'Miami, FL', 'Atlanta, GA', 'Dallas, TX'
    ]
    return random.choice(locations)

def generate_company_size():
    """Generate realistic company sizes"""
    sizes = [
        '1-10 employees', '11-50 employees', '51-200 employees',
        '201-500 employees', '501-1000 employees', '1000+ employees'
    ]
    weights = [20, 25, 25, 15, 10, 5]  # Weighted towards smaller companies
    return random.choices(sizes, weights=weights)[0]

def detect_growth_signals(company_name, industry):
    """Detect growth signals from company characteristics"""
    signals = []
    
    # Industry-based growth signals
    if industry == 'SaaS/Tech':
        signals.append('Tech sector growth')
        if 'ai' in company_name.lower() or 'ml' in company_name.lower():
            signals.append('AI/ML trending')
    
    # Company name indicators
    if any(word in company_name.lower() for word in ['cloud', 'saas', 'platform']):
        signals.append('Cloud adoption')
    
    # Random growth signals for demo
    growth_signals = [
        'Recent funding round', 'Hiring expansion', 'New product launch',
        'Market expansion', 'Partnership announcements', 'User growth'
    ]
    
    # Add 1-2 random growth signals
    num_signals = random.randint(0, 2)
    additional_signals = random.sample(growth_signals, min(num_signals, len(growth_signals)))
    signals.extend(additional_signals)
    
    return ', '.join(signals) if signals else 'None detected'

def generate_company_description(company_name, industry):
    """Generate a realistic company description"""
    templates = {
        'SaaS/Tech': f"{company_name} is a leading technology company providing innovative software solutions to help businesses streamline their operations and drive growth.",
        'Healthcare': f"{company_name} is a healthcare technology company focused on improving patient outcomes through cutting-edge medical solutions and digital health platforms.",
        'Financial Services': f"{company_name} is a financial technology company offering modern banking and payment solutions to businesses and consumers.",
        'E-commerce': f"{company_name} is an e-commerce platform connecting buyers and sellers through innovative marketplace technology and logistics solutions.",
        'Manufacturing': f"{company_name} is a manufacturing company specializing in industrial solutions and production optimization technologies.",
        'Other': f"{company_name} is a growing company providing essential services to businesses across various industries."
    }
    
    return templates.get(industry, templates['Other'])

def calculate_acquisition_fit_score(company_data):
    """Calculate AI-powered acquisition fit score (0-100)"""
    score = 0
    
    # Revenue scoring (30 points max)
    revenue_range = company_data.get('revenue_range', '')
    if revenue_range == 'High ($1M+)':
        score += 30
    elif revenue_range == 'Medium ($100K-$1M)':
        score += 15
    elif revenue_range == 'Low (<$100K)':
        score += 5
    
    # Industry scoring (20 points max)
    industry = company_data.get('industry', '')
    if industry in ['SaaS/Tech', 'Financial Services']:
        score += 20
    elif industry in ['Healthcare', 'E-commerce']:
        score += 15
    elif industry in ['Manufacturing']:
        score += 10
    else:
        score += 5
    
    # Growth signals scoring (20 points max)
    growth_signals = company_data.get('growth_signals', '')
    if 'Recent funding round' in growth_signals:
        score += 15
    if 'Hiring expansion' in growth_signals or 'Market expansion' in growth_signals:
        score += 10
    if 'New product launch' in growth_signals or 'User growth' in growth_signals:
        score += 10
    if 'AI/ML trending' in growth_signals or 'Cloud adoption' in growth_signals:
        score += 10
    
    # Cap growth signals at 20 points
    score = min(score, score - max(0, (score - 20) if growth_signals else 0))
    
    # Contact quality scoring (10 points max)
    email = company_data.get('email', '')
    phone = company_data.get('phone', '')
    linkedin = company_data.get('linkedin', '')
    
    if email and email != '':
        score += 5
    if phone and phone != '':
        score += 3
    if linkedin and linkedin != '':
        score += 2
    
    # Company size scoring (10 points max)
    company_size = company_data.get('company_size', '')
    if '1000+' in company_size:
        score += 10
    elif '501-1000' in company_size:
        score += 8
    elif '201-500' in company_size:
        score += 6
    elif '51-200' in company_size:
        score += 4
    elif '11-50' in company_size:
        score += 2
    
    # Location scoring (10 points max)
    location = company_data.get('location', '')
    tech_hubs = ['San Francisco', 'New York', 'Austin', 'Seattle', 'Boston']
    if any(hub in location for hub in tech_hubs):
        score += 10
    elif 'CA' in location or 'NY' in location or 'TX' in location:
        score += 5
    
    # Ensure score is between 0 and 100
    return min(100, max(0, score))

def enrich_leads(company_name, domain=None):
    """Main function to enrich lead data"""
    try:
        # Search for company information
        company_data = search_company_info(company_name, domain)
        
        # Calculate acquisition fit score
        score = calculate_acquisition_fit_score(company_data)
        company_data['acquisition_score'] = score
        
        return company_data
        
    except Exception as e:
        # Return minimal data structure
        return {
            'company_name': company_name,
            'domain': domain or '',
            'email': '',
            'phone': '',
            'linkedin': '',
            'industry': 'Unknown',
            'location': '',
            'company_size': '',
            'revenue_range': 'Unknown',
            'growth_signals': '',
            'description': '',
            'acquisition_score': 0
        }

# For testing purposes
if __name__ == "__main__":
    # Test the enrichment and scoring
    test_companies = [
        "Acme Software Solutions",
        "TechCorp Inc",
        "HealthTech Innovations"
    ]
    
    for company in test_companies:
        print(f"\nTesting {company}:")
        result = enrich_leads(company)
        print(f"Score: {result['acquisition_score']}")
        print(f"Industry: {result['industry']}")
        print(f"Revenue: {result['revenue_range']}")
        print(f"Email: {result['email']}")
        print(f"Growth Signals: {result['growth_signals']}")

