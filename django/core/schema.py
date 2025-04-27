import graphene

import annotation.schema
import common.schema
import image.schema


class Query(
#    annotation.schema.Query,
    common.schema.Query,
    image.schema.Query,
    graphene.ObjectType,
):
    # Combine the queries from different apps
    pass


class Mutation(
#    annotation.schema.Mutation,
    common.schema.Mutation,
    image.schema.Mutation,
    graphene.ObjectType,
):
    # Combine the mutations from different apps
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
