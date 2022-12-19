# Datadog::Monitors::Monitor MonitorFormulaAndFunctionEventQueryDefinition

A formula and functions events query.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#datasource" title="DataSource">DataSource</a>" : <i>String</i>,
    "<a href="#search" title="Search">Search</a>" : <i><a href="monitorformulaandfunctioneventquerydefinition.md">MonitorFormulaAndFunctionEventQueryDefinition</a></i>,
    "<a href="#indexes" title="Indexes">Indexes</a>" : <i>[ String, ... ]</i>,
    "<a href="#compute" title="Compute">Compute</a>" : <i><a href="monitorformulaandfunctioneventquerydefinition.md">MonitorFormulaAndFunctionEventQueryDefinition</a></i>,
    "<a href="#groupby" title="GroupBy">GroupBy</a>" : <i>[ <a href="monitorformulaandfunctioneventquerygroupby.md">MonitorFormulaAndFunctionEventQueryGroupBy</a>, ... ]</i>,
    "<a href="#name" title="Name">Name</a>" : <i>String</i>
}
</pre>

### YAML

<pre>
<a href="#datasource" title="DataSource">DataSource</a>: <i>String</i>
<a href="#search" title="Search">Search</a>: <i><a href="monitorformulaandfunctioneventquerydefinition.md">MonitorFormulaAndFunctionEventQueryDefinition</a></i>
<a href="#indexes" title="Indexes">Indexes</a>: <i>
      - String</i>
<a href="#compute" title="Compute">Compute</a>: <i><a href="monitorformulaandfunctioneventquerydefinition.md">MonitorFormulaAndFunctionEventQueryDefinition</a></i>
<a href="#groupby" title="GroupBy">GroupBy</a>: <i>
      - <a href="monitorformulaandfunctioneventquerygroupby.md">MonitorFormulaAndFunctionEventQueryGroupBy</a></i>
<a href="#name" title="Name">Name</a>: <i>String</i>
</pre>

## Properties

#### DataSource

Data source for event platform-based queries.

_Required_: Yes

_Type_: String

_Allowed Values_: <code>rum</code> | <code>ci_pipelines</code> | <code>ci_tests</code> | <code>audit</code> | <code>events</code> | <code>logs</code> | <code>spans</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Search

_Required_: Yes

_Type_: <a href="monitorformulaandfunctioneventquerydefinition.md">MonitorFormulaAndFunctionEventQueryDefinition</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Indexes

An array of index names to query in the stream. Omit or use `[]` to query all indexes at once.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Compute

_Required_: Yes

_Type_: <a href="monitorformulaandfunctioneventquerydefinition.md">MonitorFormulaAndFunctionEventQueryDefinition</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### GroupBy

Group by options.

_Required_: Yes

_Type_: List of <a href="monitorformulaandfunctioneventquerygroupby.md">MonitorFormulaAndFunctionEventQueryGroupBy</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Name

Name of the monitor

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

