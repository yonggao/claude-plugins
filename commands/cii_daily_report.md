---
description: Generate daily report for CII (Cloud Intelligence Institute) from Lark bitable data
allowed-tools: MCP,Read, Write, Bash(date)
---

# CII Daily Report Generator

Generate the latest daily report for Cloud Intelligence Institute following
these steps:

## Prerequisites Check

- recall if bitable information is present in the memory, if not then
- Ensure Lark MCP server is configured and accessible
- Verify access to "日报汇总_云智慧研究院" bitable

## Current Date Context

Please follow below examples to assign filter values while using
bitable_v1_appTableRecord_search:

```json
{
  "filter": {
    "conjunction": "and",
    "conditions": [
      {
        "field_name": "日报提交日期",
        "operator": "is",
        "value": ["Today"]
      }
    ]
  }
}
```

```json
{
  "filter": {
    "conjunction": "and",
    "conditions": [
      {
        "field_name": "日报提交日期",
        "operator": "is",
        "value": ["Yesterday"]
      }
    ]
  }
}
```

## Report Generation Process

### Step 1: Locate Data Source

Search for the Lark document named "日报汇总_云智慧研究院" to:

- Identify the correct bitable base
- Locate the appropriate table containing daily reports

### Step 2: Data Validation

Check for today's records across all departments:

- **云平台开发部** (Cloud Platform Development)
- **综合能源平台开发部** (Integrated Energy Platform Development)
- **大数据开发部** (Big Data Development)

**Important**: If ANY department above has not submitted today's report then
switch to check for yesterday's. If still not satisfied:

- ❌ **STOP execution immediately**
- 📋 List which departments have submitted reports
- 📋 List which departments are missing reports
- 🚫 Do not proceed with report generation

### Step 3: Personal Task Confirmation

Before generating the report, check if the related information is provided
otherwise search from feishu/lark calendar and task list to compose personal
part as below.

### Step 4: Report Generation

Generate the daily report in Chinese using this exact format:

```
潘永高-{YYYY.MM.DD}工作日报

一．个人重点工作
{Insert personal part here}

二．团队重点工作
1、云平台开发部
{Summarize from bitable important task field}

2、综合能源平台开发部
{Summarize from bitable important task field}

3、大数据开发部
{Summarize from bitable important task field}
```

## Quality Guidelines

### Content Requirements

- Use **Chinese** for all content
- Keep summaries **concise but informative**
- Maintain **professional tone**
- Preserve **progress percentages** and **metrics** where available

### Format Standards

- Use consistent numbering (1、2、3、)
- Include department names exactly as shown
- Maintain proper spacing and structure
- Ensure date format matches: YYYY.MM.DD

## Error Handling

If any step fails:

1. **Document Search Failure**: Report
   "无法找到日报汇总文档，请检查文档名称和访问权限"
2. **Missing Data**: Report "今日部分部门尚未提交日报: [list missing
   departments]"
3. **MCP Connection Issues**: Report "Lark MCP连接异常，请检查配置"

## Output

- Generate the formatted daily report as a markdown code block
