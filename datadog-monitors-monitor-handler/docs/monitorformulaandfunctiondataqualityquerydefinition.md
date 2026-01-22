# Datadog::Monitors::Monitor MonitorFormulaAndFunctionDataQualityQueryDefinition

A formula and functions data quality query.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#name" title="Name">Name</a>" : <i>String</i>,
    "<a href="#datasource" title="DataSource">DataSource</a>" : <i>String</i>,
    "<a href="#schemaversion" title="SchemaVersion">SchemaVersion</a>" : <i>String</i>,
    "<a href="#measure" title="Measure">Measure</a>" : <i>String</i>,
    "<a href="#filter" title="Filter">Filter</a>" : <i>String</i>,
    "<a href="#scope" title="Scope">Scope</a>" : <i>String</i>,
    "<a href="#groupby" title="GroupBy">GroupBy</a>" : <i>[ <a href="monitorformulaandfunctioneventquerygroupby.md">MonitorFormulaAndFunctionEventQueryGroupBy</a>, ... ]</i>,
    "<a href="#monitoroptions" title="MonitorOptions">MonitorOptions</a>" : <i><a href="monitorformulaandfunctiondataqualitymonitoroptions.md">MonitorFormulaAndFunctionDataQualityMonitorOptions</a></i>
}
</pre>

### YAML

<pre>
<a href="#name" title="Name">Name</a>: <i>String</i>
<a href="#datasource" title="DataSource">DataSource</a>: <i>String</i>
<a href="#schemaversion" title="SchemaVersion">SchemaVersion</a>: <i>String</i>
<a href="#measure" title="Measure">Measure</a>: <i>String</i>
<a href="#filter" title="Filter">Filter</a>: <i>String</i>
<a href="#scope" title="Scope">Scope</a>: <i>String</i>
<a href="#groupby" title="GroupBy">GroupBy</a>: <i>
      - <a href="monitorformulaandfunctioneventquerygroupby.md">MonitorFormulaAndFunctionEventQueryGroupBy</a></i>
<a href="#monitoroptions" title="MonitorOptions">MonitorOptions</a>: <i><a href="monitorformulaandfunctiondataqualitymonitoroptions.md">MonitorFormulaAndFunctionDataQualityMonitorOptions</a></i>
</pre>

## Properties

#### Name

The name of the query for use in formulas.

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### DataSource

Data source for data quality queries.

_Required_: Yes

_Type_: String

_Allowed Values_: <code>data_quality_metrics</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### SchemaVersion

Schema version for the data quality query.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Measure

The data quality measure to query. Common values include bytes, cardinality, custom, freshness, max, mean, min, nullness, percent_negative, percent_zero, row_count, stddev, sum, uniqueness. Additional values may be supported.

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Filter

Filter expression used to match on data entities. Uses Aastra query syntax.

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Scope

Optional scoping expression to further filter metrics.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### GroupBy

_Required_: No

_Type_: List of <a href="monitorformulaandfunctioneventquerygroupby.md">MonitorFormulaAndFunctionEventQueryGroupBy</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### MonitorOptions

Monitor configuration options for data quality queries.

_Required_: No

_Type_: <a href="monitorformulaandfunctiondataqualitymonitoroptions.md">MonitorFormulaAndFunctionDataQualityMonitorOptions</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

