{{/*
Expand the name of the chart.
*/}}
{{- define "todo-chatbot.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "todo-chatbot.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "todo-chatbot.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo-chatbot.labels" -}}
helm.sh/chart: {{ include "todo-chatbot.chart" . }}
{{ include "todo-chatbot.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "todo-chatbot.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-chatbot.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Backend name
*/}}
{{- define "todo-chatbot.backend.name" -}}
{{- default (printf "%s-backend" .Chart.Name) .Values.backend.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Backend fullname
*/}}
{{- define "todo-chatbot.backend.fullname" -}}
{{- if .Values.backend.fullnameOverride }}
{{- .Values.backend.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default (printf "%s-backend" .Chart.Name) .Values.backend.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Backend labels
*/}}
{{- define "todo-chatbot.backend.labels" -}}
helm.sh/chart: {{ include "todo-chatbot.chart" . }}
{{ include "todo-chatbot.backend.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Backend selector labels
*/}}
{{- define "todo-chatbot.backend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-chatbot.backend.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
MCP Server name
*/}}
{{- define "todo-chatbot.mcpServer.name" -}}
{{- default (printf "%s-mcp-server" .Chart.Name) .Values.mcpServer.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
MCP Server fullname
*/}}
{{- define "todo-chatbot.mcpServer.fullname" -}}
{{- if .Values.mcpServer.fullnameOverride }}
{{- .Values.mcpServer.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default (printf "%s-mcp-server" .Chart.Name) .Values.mcpServer.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
MCP Server labels
*/}}
{{- define "todo-chatbot.mcpServer.labels" -}}
helm.sh/chart: {{ include "todo-chatbot.chart" . }}
{{ include "todo-chatbot.mcpServer.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
MCP Server selector labels
*/}}
{{- define "todo-chatbot.mcpServer.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-chatbot.mcpServer.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Frontend name
*/}}
{{- define "todo-chatbot.frontend.name" -}}
{{- default (printf "%s-frontend" .Chart.Name) .Values.frontend.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Frontend fullname
*/}}
{{- define "todo-chatbot.frontend.fullname" -}}
{{- if .Values.frontend.fullnameOverride }}
{{- .Values.frontend.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default (printf "%s-frontend" .Chart.Name) .Values.frontend.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Frontend labels
*/}}
{{- define "todo-chatbot.frontend.labels" -}}
helm.sh/chart: {{ include "todo-chatbot.chart" . }}
{{ include "todo-chatbot.frontend.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Frontend selector labels
*/}}
{{- define "todo-chatbot.frontend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-chatbot.frontend.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}