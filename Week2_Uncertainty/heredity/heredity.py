import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def get_genes(person, one_gene, two_genes):
    """
    One person can have 0, 1 or 2 copies of the hearing impairment gene.
    Return the number of copies of the gene that a person has 
    knowing that:
    - if the person is in one_gene set -> has 1 copy of the gene 
    - if the person is in the two_genes set -> has 2 copies of the gene
    - and if it's not in either of them -> has 0 copies of the gene
    """

    if person in one_gene:
        return 1
    elif person in two_genes:
        return 2
    else:
        return 0



def get_inherit_genes(parent_genes):
    """
    Return the probability that the gene will be passed to the child 
    based on the number of the copies of the gene that the parent has and probability 
    of undergoing additional mutation
    """

    # if parent has two copies:
    #  - will pass the mutated gene on to the child
    #  - so the child will get the gene with probability 0.99 (1 - PROBS["mutation"])
    #  - will not get the gene with probability PROBS["mutation"]
    # if parent has one copy:
    #  - the gene is passed on to the child with probability 0.5
    # if parent has no copies:
    #  - will not pass the mutated gene on to the child
    #  - so the child will get the gene with probability PROBS["mutation"]
    # -  will not get the gene with probability 0.99 ( 1 - PROBS["mutation"])
    if parent_genes == 2:
        return 1 - PROBS["mutation"]
    elif parent_genes == 1:
        return (1 - PROBS["mutation"]) * 0.5
    else:
        return PROBS["mutation"]



def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    
    # to obtain joint probability, multiply the probability 
    # of all of the events taking place
    joint_p = 1

    # compute the probability for each individual member of the family 
    for member in people:
        p = 1
        
        # get the number of copies of the gene that the member has
        genes = get_genes(member, one_gene, two_genes)
        
        # check if the member has the trait or not 
        if member in have_trait:
            has_trait = True
        else:
            has_trait = False

        # get the probability of having or not the trait given 
        # the number of copies of the gene the member has
        trait_p = PROBS["trait"][genes][has_trait]

        # check if the member has parents that we know of 
        mother = people[member]["mother"]
        father = people[member]["father"]

        # if the member does not have parents registered,
        # use the unconditional probabilities for having the gene
        if not mother and not father:
            p *= PROBS["gene"][genes] * trait_p
        else:
            # if they have parents registered
            # check how many copies of the gene each parent has
            genes_mother = get_genes(mother, one_gene, two_genes)
            genes_father = get_genes(father, one_gene, two_genes)

            # based on the number of copies of genes for each parent 
            # get the probability with which the child will inherit 1 copy of the gene 
            # from each parent
            inherit_genes_mother = get_inherit_genes(genes_mother)
            inherit_genes_father = get_inherit_genes(genes_father)

            # if the child member has two copies
            # gets 1 copy of the gene from each parent 
            # if the child member has 1 copy:
            # Either he gets the gene from his mother and not his father, or he gets the gene from his father and not his mother
            # so we add both cases together
            if genes == 2:
                p *= inherit_genes_mother * inherit_genes_father * trait_p
            elif genes == 1:
                p *= ((1 - inherit_genes_mother) * inherit_genes_father + (1 - inherit_genes_father) * inherit_genes_mother) * trait_p
            else:
                p *= (1 - inherit_genes_mother) * (1 - inherit_genes_father) * trait_p

        # add the member's probability to the joint probability
        joint_p *= p

    
    return joint_p



def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    
    # for each member in probabilities, get the number of copies of the gene 
    # and if they have the trait or not 
    for member in probabilities:
        genes = get_genes(member, one_gene, two_genes)
        if member in have_trait:
            has_trait = True
        else:
            has_trait = False

        # update the current probabilities distribution wuth the new 
        # joint distribution
        probabilities[member]["gene"][genes] += p
        probabilities[member]["trait"][has_trait] += p



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    
    # make sure all values within each distribution add up to 1
    # get their sum and divide each probability by this sum to get the proportion it has within the sum
    for member in probabilities:
        sum_genes = sum([value for value in probabilities[member]["gene"].values()])
        sum_traits = sum([value for value in probabilities[member]["trait"].values()])

        for gene_num in probabilities[member]["gene"]:
            probabilities[member]["gene"][gene_num] /= sum_genes

        for trait_num in probabilities[member]["trait"]:
            probabilities[member]["trait"][trait_num] /= sum_traits


if __name__ == "__main__":
    main()
