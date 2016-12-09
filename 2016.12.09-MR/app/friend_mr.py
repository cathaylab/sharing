rows = sc.textFile("file:/Users/rongqichen/Documents/programs/DTAG-sharing/2016.12.09-MR/app/friend.txt")

def make_relation(x):
    me, friends = re.split("\s+", x.strip())
    return (me, friends.split(","))

def make_tuple(x):
    one, two = x[0], x[1]
    if one < two:
        return ("{}-{}".format(one, two), 1)
    else:
        return ("{}-{}".format(two, one), 1)

relations = rows.map(make_relation).flatMapValues(lambda x: x)
many_relations = relations.map(make_tuple).reduceByKey(lambda x,y: x+y)
both_relation = many_relations.filter(lambda x: x[1] > 1)

for relation in both_relation.collect():
    print relation
