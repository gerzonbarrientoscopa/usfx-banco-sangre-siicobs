import graphene
import graphql_jwt
import donors.schema_donations
import donations.schema
import sieves.schema
import extractions.schema
import packages.schema
import refreshments.schema
import laboratories.schema
import fragmentations.schema
import promotions.schema
import users.schema
import settings.schema
import distributions.schema
import provisions.schema
import insurance.schema

import users.mutation
import donors.mutation
import donations.mutation
import sieves.mutation
import extractions.mutation
import promotions.mutation
import distributions.mutation
import provisions.mutation
import refreshments.mutation
import fragmentations.mutation
import laboratories.mutation
import packages.mutation
from graphene_django_extras import all_directives


class Mutation(users.mutation.Mutation, donors.mutation.Mutation, donations.mutation.Mutation, sieves.mutation.Mutation,
               extractions.mutation.Mutation, refreshments.mutation.Mutation,
               fragmentations.mutation.Mutation, laboratories.mutation.Mutation, promotions.mutation.Mutation,
               packages.mutation.Mutation, distributions.mutation.Mutation, provisions.mutation.Mutation,
               graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(users.schema.Query, donors.schema_donations.Query, donations.schema.Query, sieves.schema.Query,
            extractions.schema.Query, refreshments.schema.Query, fragmentations.schema.Query, laboratories.schema.Query,
            promotions.schema.Query, provisions.schema.Query, packages.schema.Query, settings.schema.Query,
            distributions.schema.Query, insurance.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query, auto_camelcase=False, mutation=Mutation, directives=all_directives)
