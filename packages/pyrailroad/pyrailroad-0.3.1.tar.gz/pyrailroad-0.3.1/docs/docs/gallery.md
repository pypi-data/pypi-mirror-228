# Diagram gallery

A simplified SELECT statement in SQL :

![SQL SELECT](images/sql_select_stmt_simple.svg)

Parameters:

```yaml
type: sql
```

```yaml
element: Sequence
items:
  - element: Arrow
    type: right
  - element: Terminal
    text: SELECT
  - element: Arrow
    type: right
  - element: OneOrMore
    item:
      element: NonTerminal
      text: column
    repeat:
      element: Sequence
      items:
        - element: Arrow
          direction: left
        - element: Terminal
          text: ','
        - element: Arrow
          direction: left
  - element: Arrow
    type: right
  - element: Terminal
    text: FROM
  - element: Arrow
    type: right
  - element: OneOrMore
    item:
      element: NonTerminal
      text: table
    repeat:
      element: Sequence
      items:
        - element: Arrow
          direction: left
        - element: Terminal
          text: ','
        - element: Arrow
          direction: left
  - element: Arrow
    type: right
  - element: Terminal
    text: WHERE
  - element: Arrow
    type: right
  - element: NonTerminal
    text: condition
```
