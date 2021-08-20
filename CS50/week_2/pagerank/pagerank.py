import copy
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
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    dist = dict()
    linked_pages = set(corpus[page])

    if len(linked_pages) == 0:  # Pretending a page had links to all pages in the corpus
        for p in corpus.keys():
            linked_pages.add(p)
    page_count = len(corpus.keys())
    link_count = len(linked_pages)

    unlinked_prob = (1 - damping_factor) / page_count
    linked_prob = (damping_factor / link_count) + unlinked_prob

    for p in corpus.keys():
        if p in linked_pages:
            dist[p] = linked_prob
        else:
            dist[p] = unlinked_prob

    print(f"Sum of values in returned distribution: {sum(dist.values())}")
    return dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    visit_count = dict()
    for page in pages:
        visit_count[page] = 0
    dist = None
    pr = {}

    for i in range(n):
        if dist is None:
            selected_page = random.choice(pages)
            dist = transition_model(corpus, selected_page, damping_factor)
        else:
            selected_page = random.choices(population=pages, weights=list(dist.values()), k=1)[0]
            visit_count[selected_page] += 1
            dist = transition_model(corpus, selected_page, damping_factor)

    for p in pages:
        pr[p] = visit_count[p] / n
    print(f"Sum of Pagerank Values: {sum(pr.values())}")
    return pr


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pr = {}
    pages = corpus.keys()
    page_count = len(pages)
    for page in pages:
        pr[page] = 1 / page_count

    error = 1
    while error >= 0.001:
        error = 0
        prev = pr.copy()
        for p in pr:
            linking_pages = [linking for linking in corpus if p in corpus[linking]]
            total = 0
            for page in linking_pages:
                total += prev[page] / len(corpus[page])
            pr[p] = ((1 - damping_factor) / page_count) + (damping_factor * total)
            if error < abs(pr[p] - prev[p]):
                error = abs(pr[p] - prev[p])
    estimated_ranks = {}
    total = sum(pr.values())
    for p, prob in pr.items():
        estimated_ranks[p] = prob/total
    print(f"Sum of Estimated Pagerank Values: {sum(estimated_ranks.values())}")
    return estimated_ranks


if __name__ == "__main__":
    main()
