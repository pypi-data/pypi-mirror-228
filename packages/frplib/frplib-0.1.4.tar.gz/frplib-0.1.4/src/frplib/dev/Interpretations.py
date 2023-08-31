#
# An Interpretation of a Model
#
# To first order, an Interpretation is a Functor
#
#   KindMonad[VecTuple[V], P] -> KindMonad[tuple[str, VecTuple[V]], P].
#
# Another way to look at this is that we annotate the leaves of a kind.
# We provide methods for summarizing calculations *on this kind* (e.g.,
# marginalization, conditional statements, ...) but *not* for generating
# new kinds from this. (That's the job of Kind.) That is, an interpretation
# freezes the kind. ATTN: need to work this out fully.  An alternative
# is to hold the annotations in a more open state (strings or functions, see below)
# and allow calculations.  Note that the mapped values must be unique for
# this to make sense (otherwise, do a transform first)
#
# Example (without annotation):
#
#   have_disease = choice(0, 1, 0.99)
#   test_result_with_disease = choice(0, 1, 0.05)
#   test_result_no_disease = choice(0, 1, 0.95)
#   test_result_by_disease = {0: test_result_no_disease, 1: test_result_with_disease}
#   
#   disease_if_test_positive = have_disease >> test_result_by_disease | (Proj(2) == 1) @ 1
#
# ATTN: Consider making Projections a subclass of statistics that maintain their
# indices and can be used in lieu of integers or index list in a marginalization.
# Last bit would be
#
#   disease = Proj(1)
#   test = Proj(2)
#    
#   disease_if_test_positive = have_disease >> test_result_by_disease | (test == 1) @ disease
#
# With annotations: an idealized version
#
#   disease_status = interpetation( KIND, {0: "Do not have the disease", 1: "Have the disease"} )
#   test_result = interpretation( KIND, lambda result: "Tests Positive" if result == 1 else "Tests Negative" )
#      # Here, the KIND (= None) is a constant that causes a function Kind -> Interpretation to be returned
#      # If given an actual kind, return the interpretation of that kind.
#    
#   have_disease = disease_status(choice(0, 1, 0.99))
#   test_result_by_disease = {"Do not have the disease": test_result(choice(0, 1, 0.95)),
#                             "Have the disease": test_result(choice(0, 1, 0.05))}
#    
#   disease = Proj(1)
#   test = Proj(2)
#      
#   disease_if_test_positive = have_disease >> test_result_by_disease | (test == 1) @ disease
#
# Producing
#    
#       +---- 99/118 ---- Do not have the disease
#       |
#   <> -+
#       |
#       +---- 19/118 ---- Have the disease
# Similarly, E detects annotation and binary values giving
#
# E(disease_if_test_positive) = Have the disease[19/118]
#
# But ATTN: this needs to be worked out.  The key innovations here:
#
#    a. Let values be associated with annotations for specifying things
#    b. Let Proj() statistics be used for marginalization
#    c. E() produces an object which can display in useful forms in special cases
#    d. The functions in interpretations are tuple safe.
#    e. Can offer helpers for constructing interpretions (e.g., label('x', '{x} widgets'))
#
# Note that for many cases, an interpretion will be a function from values to strings;
# like  lambda x,y: f'point at ({x},{y})' or lambda sold_count: f'Sold {sold_count} widgets'
#
# An interpretation of dimension d is specified as either:
#
# 1. A function from a values to annotations  (must be total on the possible values of the kind but can accept other values if convenient)
# 2. A dict mapping to values to annotations  (keys must contain all values of the kind, but can have others if convenient which will be ignored)
# 2. An array of length d whose elements are 1-dim versions of #1 and #2
#

# NOTE: It's possible that we can use metaclasses to create an interpretation DSL
#
# Consider for instance based on the above example the following
#
# class My(Components):
#     DISEASE = 1
#     TEST = 2
#
# This looks like an enum but  DISEASE and TEST define Proj() statistics
# that can be used in test and marginalization
#
#  ... | (TEST = 2) @ DISEASE
#
# The 'class My()' is a bit awkward and boilerplate-y, but we can think about it
# pretty clearly...
#
# We can go further:
#
#
# class MyModel(Interpretation):
#
#    DISEASE = 1
#    TEST = 2
#
#    def ...():
#        ...
#
# with def'd methods here giving interpreations
# or
#    


# From old Model.py
#
# A Model is an "interpretation" of the values in an FRP.
# We specify a mapping from values to interpretations.
# The result is that the normal output functions for FRPs
# show the interpretations instead of the values, making
# for a nice display *and* showing the modeling procedure.
#
# Modeling can be done at the value level or the component level,
# so we need constructors for each.
#
# Note: In general for models and transforms, we treat
# dicts with value tuples as keys as functions defined
# on the FRPs value set. (Define values(X) and kind(X)
# in the text also.)  So you can give a function
# from values to interpretations here, or you can give
# a dict acting as a mapping of the same type
# 
#
# This is why we keep tuples as keys as they are hashable.
#

