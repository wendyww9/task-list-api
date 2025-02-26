# Optional Enhancements

## Goal

Optional enhancements are meant to spark our imagination! They can give us extra ideas for how to extend this project. Optional enhancements should never compromise the project requirements, unless there are special circumstances.

## Optional Means Optional

It is more important and more valuable to do good work with the requirements, and to solidify your learning. Please do not work on optional enhancements before feeling confident in the project requirements.

## Prompts

### Edge Cases

Many waves are missing many edge case considerations. Consider different edge cases in each wave, make decisions for what should happen, and then implement it!

As inspiration, here are some beginning edge cases to consider:

What should happen if...

- when creating a task, the value of `completed_at` is a string that is not a datetime?
- when updating a task, the value of `completed_at` is a string that is not a datetime?
- when getting all tasks, and using query params, the value of `sort` is not "desc" or "asc"?

For each of these, consider what the HTTP response should be.

How would you write tests for it? How would you implement it?

Your decisions should not break the other tests.

### Use List Comprehensions

Use list comprehensions in your route functions where applicable.

### More Query Params

Create the tests and implementation so that the user may

- filter tasks by title
- sort tasks by id
- sort goals by title

Remember that Wave 2 already has a sorting feature for tasks by title, so we might practice creating another route helper method that can be used for sorting across multiple model types. Such a method could even be extended to perform the filtering as well!