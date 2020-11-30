from clips import Environment, Symbol

environment = Environment()

# assert a fact as string
environment.assert_string('(a-fact)')

# retrieve a fact template
template = environment.find_template('a-fact')

# create a new fact from the template
fact = template.new_fact()

# implied (ordered) facts are accessed as lists
fact.extend((7, 2))

# assert the fact within the environment
fact.assertit()

# execute the activations in the agenda
environment.run()
for fact in environment.facts():
    print(fact)