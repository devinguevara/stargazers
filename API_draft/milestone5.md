The API draft in the folder was found to be sufficiently complete given the SRS requirements laid out at the beginning of the assignment in the signed agreement. 
No modifications to the diagram or document were required.

Integration tests are included on the dev branch, including GitHub Actions for the modules `metadata_extraction`, `augment`, and more. 
The API was not modified because the flexibility of the agreed-upon SRS requirements in the documents we signed allowed us to specify the modules
and functions we planned to complete early on. Functionality and usability are emphasized; in particular, modules such as `augment` and `ml_stargazer` 
allow the user to choose the variables for which they plan to apply differentegrals or ML classification methods. The user is allowed
the flexibility to apply their astronomy knowledge in making these statistical decisions.

Each module which performs a calculation or operation is designed to perform in conjunction with the output of the query and preprocessing modules, which return 
a `pd.DataFrame` in a specific format in order to ensure seamless integration with other modules in the `stargazer` package.

The specific continuous integration tests can be found in the folder `.github/workflows/` in the dev (and main) branch; previous runs are viewable in GitHub Actions tab.
