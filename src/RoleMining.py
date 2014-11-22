
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

Roles = enum("OUTSIDER", "LEADER", "OUTERMOST", "MEDIATOR")


class RoleMining(object):

    def __init__(self, network):
        self.network = network

    def find_outsiders(self):
        # depends on the grouping, probably the ones without
        pass
        # for comm in sorted(self.communities.values(), key=len):
        #     print len(comm)
        #     if len(comm) == 1:
        #         print "outsider: ", comm[0]



