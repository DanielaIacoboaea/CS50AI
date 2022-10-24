import os
import random
import re
import sys
import copy
from collections import Counter

DAMPING = 0.85
SAMPLES = 10000
ACCURACY = 0.001


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
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # every page gets the probability of being chosen randomly among all pages inside corpus
    distribution = dict()
    probability_for_all = (1 - damping_factor)/len(corpus)

    for title in corpus:
        distribution[title] = probability_for_all
    
    # add to that the probability of being chosen randomly as a next link from the current page  
    if page in corpus:
        if len(corpus[page]):
            for link in corpus[page]:
                distribution[link] += damping_factor/len(corpus[page])
    
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Keep each sample randomly generated in states
    # probability damping_factor -> randomly choose one of the links from page with equal probability 
    # probability 1 - damping_factor -> randomly choose one of all pages in the corpus with equal probability
    # e.g for corpus: {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}:
    # damping_factor = 0.85
    # transition model is: {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}
    ranks = dict()
    states = []

    # every page gets the probability of choosing randomly among all pages inside corpus
    probability_for_all = (1 - damping_factor)/len(corpus)

    # check if a page has no outgoing links to other pages 
    # and add links to all pages in the corpus, including itself
    copy_corpus = copy.deepcopy(corpus)
    for page_name in copy_corpus:
        if not len(copy_corpus[page_name]):
            for link in copy_corpus:
                copy_corpus[page_name].add(link)

    # generate first page/sample randomly
    p = []
    for i in range(len(copy_corpus)):
        p.append(probability_for_all)

    first_page = random.choices([page for page in copy_corpus.keys()], weights=p, k=1)
    states.append(first_page[0])

    # generate n - 1 samples from the first page
    current_page = first_page[0]
    for sample in range(n-1):
        distribution = transition_model(copy_corpus, current_page, damping_factor)
        pages = []
        probabilities = []
        for page, p in distribution.items():
            pages.append(page)
            probabilities.append(p)
        next_page = random.choices(pages, weights=probabilities, k=1)
        states.append(next_page[0])
        current_page = next_page[0]
    
    # count how many times each page was randomly selected in states
    # and compute it's PageRank
    page_count = Counter(states)
    for page, count in page_count.items():
        ranks[page] = count/n

    return ranks
    


def check_convergence(prev_ranks, new_ranks):
    """
    Check if the PageRank values change by more than 0.001 between the previous rank values
    and the new rank values for each page within state.
    """

    for page in new_ranks:
        if abs(new_ranks[page] - prev_ranks[page]) > ACCURACY:
            return False

    return True



def apply_formula(corpus, page, damping_factor, ranks):
    """
    Generate a new PageRank for one page within the state based on previous ranks.
    Return the new page rank
    """

    rand_prob = (1 - damping_factor)/len(corpus)
    links_prob = []

    links = []

    # gather all pages that have outgoing links to this page
    # assumption: a page without outgoing links has links to all pages including itself
    # so links will never be empty
    for page_name in corpus:
        if page in corpus[page_name]:
            links.append(page_name)
    
    # compute the probability of reaching to this page from each page with outgoing links here 
    # by dividing each page's individual PageRank to the number of links within the page   
    if links:
        for link in links:
            if len(corpus[link]):
                links_prob.append(ranks[link]/len(corpus[link]))
            else:
                links_prob.append(ranks[link])

    # add all probabilities  
    pageRank = rand_prob + damping_factor * sum(links_prob)
    return round(pageRank, 5)



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # keep previous state in ranks 
    # keep new state in new_ranks
    # transition from previous state to new state using the PageRank formula 
    # and iterative algorithm
    ranks = dict()
    new_ranks = dict()

    # in initial state we assume each PageRank is 1/N (equally likely to be on any page)
    initial_prob = 1/len(corpus)

    # check if a page has no outgoing links to other pages 
    # and add links to all pages in the corpus, including itself
    copy_corpus = copy.deepcopy(corpus)
    for page_name in copy_corpus:
        if not len(copy_corpus[page_name]):
            for link in copy_corpus:
                copy_corpus[page_name].add(link)

    for page in copy_corpus:
        ranks[page] = initial_prob
    
    # generate next state with updated PageRanks based on formula
    for page in copy_corpus:
        new_ranks[page] = apply_formula(copy_corpus, page, damping_factor, ranks)

    # generate states until the difference in PageRanks for all pages 
    # is less than 0.001 from previous state to new state
    while not check_convergence(ranks, new_ranks):
        ranks.clear()
        ranks = new_ranks.copy()
        new_ranks.clear()
        for page in copy_corpus:
            new_ranks[page] = apply_formula(copy_corpus, page, damping_factor, ranks)

    return new_ranks


if __name__ == "__main__":
    main()
