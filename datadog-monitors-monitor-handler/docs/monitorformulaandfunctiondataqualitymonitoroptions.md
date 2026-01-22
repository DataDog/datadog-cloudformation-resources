# Datadog::Monitors::Monitor MonitorFormulaAndFunctionDataQualityMonitorOptions

Monitor configuration options for data quality queries.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#customsql" title="CustomSql">CustomSql</a>" : <i>String</i>,
    "<a href="#customwhere" title="CustomWhere">CustomWhere</a>" : <i>String</i>,
    "<a href="#groupbycolumns" title="GroupByColumns">GroupByColumns</a>" : <i>[ String, ... ]</i>,
    "<a href="#crontaboverride" title="CrontabOverride">CrontabOverride</a>" : <i>String</i>,
    "<a href="#modeltypeoverride" title="ModelTypeOverride">ModelTypeOverride</a>" : <i>String</i>
}
</pre>

### YAML

<pre>
<a href="#customsql" title="CustomSql">CustomSql</a>: <i>String</i>
<a href="#customwhere" title="CustomWhere">CustomWhere</a>: <i>String</i>
<a href="#groupbycolumns" title="GroupByColumns">GroupByColumns</a>: <i>
      - String</i>
<a href="#crontaboverride" title="CrontabOverride">CrontabOverride</a>: <i>String</i>
<a href="#modeltypeoverride" title="ModelTypeOverride">ModelTypeOverride</a>: <i>String</i>
</pre>

## Properties

#### CustomSql

Custom SQL query for the monitor.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### CustomWhere

Custom WHERE clause for the query.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### GroupByColumns

Columns to group results by.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### CrontabOverride

Crontab expression to override the default schedule.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### ModelTypeOverride

Override for the model type used in anomaly detection.

_Required_: No

_Type_: String

_Allowed Values_: <code>freshness</code> | <code>percentage</code> | <code>any</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

