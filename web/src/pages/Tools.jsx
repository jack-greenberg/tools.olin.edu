import React from "react";
import { useQuery } from "@apollo/react-hooks";
import gql from "graphql-tag";

import _ from "lodash";

const toolQuery = gql`
  query {
    tools {
      id
      name
      category {
        name
      }
    }
  }
`

const Tools = () => {
  const { loading, error, data } = useQuery(toolQuery);

  if (loading) {
    return (
      <div>
        Loading...
      </div>
    )
  }

  if (error) {
    // Handle error
  }

  const sorted = _.groupBy(data.tools,"category.name");

  const toolList = Object.keys(sorted).map((category) => {
    const tools = sorted[category];
    const toolItems = tools.map(tool => {
      return (
        <li data-id={tool.id} key={tool.id}>
          {tool.name}
        </li>
      )
    })

    return (
      <div key={category}>
        <h3>{category}</h3>
        <ul>
          {toolItems}
        </ul>
      </div>
    )
  });

  return (
    <div>
      {toolList}
    </div>
  )
}

export default Tools;
