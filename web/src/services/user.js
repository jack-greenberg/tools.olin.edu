import { ApolloClient, InMemoryCache, gql } from '@apollo/client';

const baseUrl = "/api/"


export const userQuery = gql`
  query getCurrentUser {
    me {
      id
      user_id
      display_name
      first_name
      last_name
      email
    }
  }
`

// export const getCurrentUser = async () => {
//   var r;
//   await client.query({ query: userQuery })
//     .then(response => {
//       r = response.data;
//     })
//     .catch(err => {
//       console.log();
//     })
// 
//   return r
// }
