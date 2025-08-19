######################################
#
# Title: morpho_helper.py
# Purpose: A helper function for the morpho agent
# Author: Nzwisisa Chidembo
# Date Created: 19 Aug 2025
# Date Updated: 19 Aug 2025
#
#######################################

'''
GraphQL endpoint: https://api.morpho.org/graphql

Query to run:
query {
  vaults(first: 20, where: { chainId_in: [1] }, orderBy: DailyApy) {
    items {
      name
      symbol
      chain {
        id
        network
      }
      state {
        dailyApy
      }
    }
  }
}
'''

import requests
import json
from typing import Dict, Any, Optional


def execute_morpho_query(
    query: str = None,
    variables: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Execute a GraphQL query against the Morpho endpoint.
    
    Args:
        query: The GraphQL query string (uses default vault query if None)
        variables: Optional variables for the query
        headers: Optional HTTP headers
        
    Returns:
        The GraphQL response as a dictionary
        
    Raises:
        requests.RequestException: If the HTTP request fails
        ValueError: If the response is not valid JSON
    """
    endpoint = "https://api.morpho.org/graphql"
    
    # Default query if none provided
    if query is None:
        query = """
        query {
          vaults(first: 20, where: { chainId_in: [1] }, orderBy: DailyApy) {
            items {
              name
              symbol
              chain {
                id
                network
              }
              state {
                dailyApy
              }
            }
          }
        }
        """
    
    payload = {
        "query": query,
        "variables": variables or {}
    }
    
    default_headers = {
        "Content-Type": "application/json",
        "User-Agent": "morpho-helper/1.0"
    }
    
    if headers:
        default_headers.update(headers)
    
    response = requests.post(
        endpoint,
        json=payload,
        headers=default_headers
    )
    
    response.raise_for_status()
    
    try:
        return response.json()
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response: {e}")


def get_vault_data() -> Dict[str, Any]:
    """
    Get vault data using the default query.
    
    Returns:
        Vault data from the Morpho API
    """
    return execute_morpho_query()


if __name__ == "__main__":
    print(type(get_vault_data()))
    print(get_vault_data())




