# mssqlgenerator
Generate CREATE, INSERT, MERGE and DELETE statements for T-SQL based on JSON Table Descriptions.

<br/>

# Table Descriptor Format

## JSON Attributes

|ATTRIBUTE/KEY|TYPE|REQUIRED|OPTIONS|DEFAULT|DESCRIPTION|
|-------------|----|:------:|------|-------|-----------|
|name|text|Yes|-|-|table name|
|dependents|array(text)|No|-|-|list of tables that import keys from this table (to be removed before CREATE TABLE)|
|fields|dict|Yes|-|-|dictionary of table columns with format {"1st column index":{...}, "2nd ...":{...}}|
|fields.\<num>|dict key|Yes|-|-|numeric key for column discription (index / to determine order of columns)|
|^.^.name|text|Yes|-|-|column name|
|^.^.type|text|Yes|MS SQL datatypes|-|column data type (MS SQL specific e.g. INT, VARCHAR)|
|^.^.type_args|array(text/num)|No|MS SQL datatype args|-|arguments passed to column type (e.g. 250 in VARCHAR(250))|
|^.^.key|boolean|No|true/false|false|to indicate if column is a primary key|
|^.^.constraints|array(text)|No|-|-|add additional constraints to column such as "not null" and "default \<value>"|
|^.^.merge_type|text|No|"replace"/"accumulate"|"replace"|behaviour in MERGE statement (does not apply to merge_on params)|
|^.^.relation|dict|No|-|-|describes foreign key relation of column with other table's column|
|^.^.^.table|text|Yes if^|-|-|relation: name of table|
|^.^.^.column|text|Yes if^|-|-|relation: name of column in table|
|^.^.^.enforce|boolean|No|true/false|true|relation: indicates whether to create constraint for this relation|
|^.^.^.on_delete|text|No|see below|-|relation: indicates ON DELETE behaviour of FK relation|
|^.^.^.on_update|text|No|see below|-|relation: indicates ON UPDATE behaviour of FK relation|
|merge_on|array(text)|Yes (for merge)|-|-|array of field names (typically table keys) which should be matched for merge to occur

<br/>

## OPTIONS for fields.\<num>.merge_type

|Value|Is Default|Identifier in App|Behaviour|
|-----|:--------:|-----------------|---------|
|"replace"|Yes|COL_MERGE_TYPE_REPLACE|replace value with new in MERGE statement|
|"accumulate"|No|COL_MERGE_TYPE_ACCUMLATE|add with new value in MERGE statement|

This attribute does not apply to columns which have been listed in the merge_on list.

<br/>

## OPTIONS for fields.\<num>.relation.on_delete / fields.\<num>.relation.on_update

|Value|Is Default|Identifier in App|Behaviour|
|-----|:--------:|-----------------|---------|
|"no action"|No|COL_RELATION_UPDEL_NO_ACTION|see below|
|"cascade"|No|COL_RELATION_UPDEL_CASCADE|see below|

Validity subject to MS SQL constraints and combination of on_delete & on_update values.

<br/>

## FK relation ON DELETE & ON UPDATE options behaviour
|Option|Update operation on parent table|Delete operation on parent table|
|------|--------------------------------|----------------|
|No Action|Not allowed.<br/>Error message would be generated.|Not allowed.<br/>Error message would be generated.|
|Cascade|Associated values in child table would also be updated.|Associated records in child table would also be deleted.|
|Set NULL|Associated values in child table would be set to NULL.<br/>Foreign key column should allow NULL values to specify this rule.   Foreign key column should allow NULL values to specify this rule.|Associated values in child table would be set to NULL.<br/>Foreign key column should allow NULL values to specify this rule.   Foreign key column should allow NULL values to specify this rule.|
|Set Default|Associated values in child table would be set to default value specified in column definition. Also default value should be present in primary key column. Otherwise basic requirement of FK relation would fail and delete operation would not be successful.<br/>If no default value is provided in foreign key column this rule could not be implemented.|Associated values in child table would be set to default value specified in column definition. Also default value should be present in primary key column. Otherwise basic requirement of FK relation would fail and delete operation would not be successful.<br/>If no default value is provided in foreign key column this rule could not be implemented.|

<br/>

## Example Table Descriptor JSON

```javascript
{
    "name": "Location",
    "dependents": ["Warehouse", "Store"],
    "fields": {
        "0": {
            "name": "id",
            "type": "INT",
            "key": true
        },
        "1": {
            "name": "name",
            "type": "VARCHAR",
            "type_args": [250],
            "merge_type": "replace",
            "constraints": ["not null"]
        },
        "2": {
            "name": "country",
            "type": "VARCHAR",
            "type_args": [50],
            "key": true,
            "relation": {
                "table": "Country",
                "column": "id",
                "enforce": true,
                "on_delete": "set null",
                "on_update": "cascade"
            }
        },
        "3": {
            "name": "owner",
            "type": "VARCHAR",
            "type_args": [250],
            "constraints": ["not null"],
            "merge_type": "replace",
            "key": false,
            "relation": {
                "table": "Person",
                "column": "id",
                "enforce": true,
                "on_delete": "no action",
                "on_update": "cascade"
            },
            "about": "sum of amount for a day, picked from stock.location.amount"
        },
        "4": {
            "name": "amount",
            "type": "NUMERIC",
            "type_args": [11, 2],
            "constraints": ["default 0"],
            "merge_type": "accumulate",
            "about": "sum of amount for a day, picked from stock.location.amount"
        }
    },
    "merge_on": ["id", "country"],
    "about": "table for stock.location"
}
```

<br/>

# Version info
|Name |Release Date|Notes|
|-----|------------|-----|
|v1.0 |22-Jan-2022 |First Version|
|v1.1 |04-Aug-2022 |Minor Bug Fixes|

<br/>

# Notes
- Text case of attribute values does not matter.
- Values with restricted set of options can use variables in options.py for consistency.
