import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
        
        # Create a dictionary to store the probability of each page
        prob = dict()
    
        # If the page has no outgoing links, then the model should return a probability distribution that chooses randomly among all pages with equal probability.
        if len(corpus[page]) == 0:
            for p in corpus:
                prob[p] = 1/len(corpus)
            return prob
    
        # If the page has outgoing links, then each link should have an equal probability of being chosen.
        for p in corpus:
            prob[p] = (1-damping_factor)/len(corpus)
    
        # The probability of choosing each page with outgoing links is the damping factor divided by the number of outgoing links.
        for p in corpus[page]:
            prob[p] += damping_factor/len(corpus[page])
    
        return prob

        

def sample_pagerank(corpus, damping_factor, n):
    
    #This function works by choosing a page at random and then choosing the next page based on the probability of each page. It repeats this process n times and then returns the probability of each page after n samples
    """"
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys()) # list of all pages
    prob = dict() # dictionary to store the probability of each page

    # Initialize the probability of each page to 0 becuase we have not chosen any page yet
    for page in pages:
        prob[page] = 0
    
    first_page = random.choice(pages) # choose a page at random
    prob[first_page] = 1/n # set the probability of the first page to 1/n because we have chosen it once where n is the number of samples and also the number of times we will choose a page

    current_prob = transition_model(corpus, first_page, damping_factor) # get the probability of each page after the first sample
    for i in range(n-1):# repeat the process n-1 times
        next_page = random.choices(pages, weights = current_prob.values(), k = 1)[0] # choose the next page based on the probability of each page
        prob[next_page] += 1/n# we are choosing the next page once, so we add 1/n to the probability of the next page so as to get the probability of the next page after n samples
        current_prob = transition_model(corpus, next_page, damping_factor) # get the probability of each page after the next sample
    print(sum(prob.values()))
    return prob # return the probability of each page after n samples

def iterate_pagerank(corpus, damping_factor):
    #This function is based on the formula given in the lecture and it works by iteratively updating the probability of each page until convergence
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    pages = list(corpus.keys()) # list of all pages
    prob = dict() # dictionary to store the probability of each page
    new_prob = dict() # dictionary to store the new probability of each page
    
        # Initialize the probability of each page to 1/N
    for page in pages:
        prob[page] = 1/len(pages)
        new_prob[page] = 0
    iterations = 0
    
        # Repeat until convergence
    while True:
        iterations +=1
        for page in pages:
            # The new probability of a page is the sum of (probability of each page that links to it * damping factor / number of links in that page) + ((1-damping factor)/N)
            new_prob[page] = sum(prob[p] * damping_factor/len(corpus[p]) for p in pages if page in corpus[p]) + (1-damping_factor)/len(pages)
        # If the difference between the new probability and the old probability of each page is less than 0.001, then we have converged
        if all(abs(new_prob[page] - prob[page]) < 0.001 for page in pages):
            break
            # If we have not converged, then the new probability of each page becomes the old probability of each page
        else:
            prob = new_prob.copy()
    print(sum(prob.values()))
    print(iterations)
    return prob # return the probability of each page after convergence


if __name__ == "__main__":
    main()
