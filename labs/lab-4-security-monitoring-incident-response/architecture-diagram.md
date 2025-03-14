# Lab 4: Security Monitoring and Incident Response - Architecture Diagram

This document provides architecture diagrams for the security monitoring and incident response solution implemented in Lab 4.

## Overall Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                                      AWS Cloud                                        │
│                                                                                      │
│  ┌──────────────────────────────────────┐      ┌───────────────────────────────────┐ │
│  │       Logging & Monitoring           │      │      Threat Detection              │ │
│  │                                      │      │                                    │ │
│  │  ┌───────────┐      ┌──────────────┐ │      │  ┌───────────┐   ┌──────────────┐ │ │
│  │  │           │      │              │ │      │  │           │   │              │ │ │
│  │  │ CloudTrail├─────▶│ CloudWatch   │ │      │  │ GuardDuty │   │ Security Hub │ │ │
│  │  │           │      │ Logs & Alarms│ │      │  │           │   │              │ │ │
│  │  └───────────┘      └──────┬───────┘ │      │  └─────┬─────┘   └───────┬──────┘ │ │
│  │                            │         │      │        │                 │        │ │
│  │  ┌───────────┐      ┌──────▼───────┐ │      │        │     ┌───────────▼──────┐ │ │
│  │  │           │      │              │ │      │        │     │                  │ │ │
│  │  │    S3     │◀─────┤  CloudWatch  │ │      │        │     │    AWS Config    │ │ │
│  │  │  Buckets  │      │  Dashboards  │ │      │        │     │                  │ │ │
│  │  │           │      │              │ │      │        │     │                  │ │ │
│  │  └───────────┘      └──────────────┘ │      │        │     └─────────┬────────┘ │ │
│  └────────────────────────┬─────────────┘      └────────┼───────────────┘          │ │
│                           │                             │                           │ │
│                           ▼                             ▼                           │ │
│  ┌──────────────────────────────────────────────────────────────────────────────┐  │ │
│  │                             Amazon EventBridge                               │  │ │
│  └────────────────────────────────────┬─────────────────────────────────────────┘  │ │
│                                        │                                            │ │
│                 ┌─────────────────────┐│┌───────────────────┐                       │ │
│                 │                     ││                    │                       │ │
│  ┌──────────────▼──────────┐   ┌──────▼▼─────────┐    ┌─────▼──────────────────┐   │ │
│  │      Notifications      │   │                 │    │   Incident Response     │   │ │
│  │                         │   │     Lambda      │    │      Automation         │   │ │
│  │  ┌─────────────────┐    │   │    Functions    │    │                         │   │ │
│  │  │                 │    │   │                 │    │  ┌────────────────────┐ │   │ │
│  │  │   Amazon SNS    │    │   │  ┌───────────┐  │    │  │  Systems Manager   │ │   │ │
│  │  │                 │    │   │  │Security   │  │    │  │   Automation       │ │   │ │
│  │  └────────┬────────┘    │   │  │Automation │  │    │  │                    │ │   │ │
│  │           │             │   │  │Functions   │  │    │  └────────────────────┘ │   │ │
│  │  ┌────────▼────────┐    │   │  └───────────┘  │    │                         │   │ │
│  │  │                 │    │   │                 │    │  ┌────────────────────┐ │   │ │
│  │  │   Email, SMS,   │    │   │                 │    │  │ Incident Response  │ │   │ │
│  │  │   Chat, etc.    │    │   │                 │    │  │     Playbooks      │ │   │ │
│  │  │                 │    │   │                 │    │  │                    │ │   │ │
│  │  └─────────────────┘    │   └─────────────────┘    │  └────────────────────┘ │   │ │
│  └─────────────────────────┘                          └─────────────────────────┘   │ │
│                                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

## Module 1: Centralized Logging and Monitoring

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        Centralized Logging and Monitoring                        │
│                                                                                 │
│  ┌───────────────┐         ┌────────────────────┐         ┌──────────────────┐  │
│  │               │         │                    │         │                  │  │
│  │  AWS CloudTrail│───────▶│ CloudWatch Logs    │────────▶│  CloudWatch      │  │
│  │  Trail        │         │                    │         │  Alarms          │  │
│  │               │         │                    │         │                  │  │
│  └───────┬───────┘         └──────────┬─────────┘         └──────────────────┘  │
│          │                            │                                          │
│          │                            │                                          │
│          ▼                            ▼                                          │
│  ┌───────────────┐         ┌────────────────────┐         ┌──────────────────┐  │
│  │               │         │                    │         │                  │  │
│  │  S3 Bucket    │         │  Metric Filters:   │         │  CloudWatch      │  │
│  │  (Encrypted)  │         │  - Root Login      │         │  Dashboard       │  │
│  │               │         │  - IAM Changes     │         │                  │  │
│  │               │         │  - SG Changes      │         │                  │  │
│  │               │         │  - Failed Logins   │         │                  │  │
│  └───────────────┘         └────────────────────┘         └──────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Module 2: Threat Detection and Alerting

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            Threat Detection and Alerting                         │
│                                                                                 │
│  ┌───────────────┐    ┌────────────────────┐    ┌────────────────────────────┐  │
│  │               │    │                    │    │                            │  │
│  │  Amazon       │───▶│  AWS Security Hub  │◀───│  AWS Config                │  │
│  │  GuardDuty    │    │                    │    │                            │  │
│  │               │    │                    │    │                            │  │
│  └───────┬───────┘    └─────────┬──────────┘    └────┬───────────────────────┘  │
│          │                      │                     │                          │
│          │                      │                     │                          │
│          ▼                      ▼                     ▼                          │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                             EventBridge Rules                              │  │
│  └───────────────────────────────────────┬───────────────────────────────────┘  │
│                                          │                                       │
│                                          │                                       │
│                                          ▼                                       │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                             Amazon SNS Topics                              │  │
│  └───────────────────────────────────────┬───────────────────────────────────┘  │
│                                          │                                       │
│                                          │                                       │
│                                          ▼                                       │
│  ┌───────────────┐    ┌────────────────────┐    ┌────────────────────────────┐  │
│  │               │    │                    │    │                            │  │
│  │  Email        │    │  SMS               │    │  Chat Applications         │  │
│  │  Notifications│    │  Notifications     │    │  (Optional)                │  │
│  │               │    │                    │    │                            │  │
│  └───────────────┘    └────────────────────┘    └────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Module 3: Incident Response Automation

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         Incident Response Automation                             │
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                         Security Event Detection                           │  │
│  │                                                                           │  │
│  │  ┌───────────────┐    ┌────────────────────┐    ┌─────────────────────┐  │  │
│  │  │               │    │                    │    │                     │  │  │
│  │  │  GuardDuty    │    │  Security Hub      │    │  AWS Config         │  │  │
│  │  │  Findings     │    │  Findings          │    │  Rule Violations    │  │  │
│  │  │               │    │                    │    │                     │  │  │
│  │  └───────┬───────┘    └─────────┬──────────┘    └─────────┬───────────┘  │  │
│  │          │                      │                         │              │  │
│  └──────────┼──────────────────────┼─────────────────────────┼──────────────┘  │
│             │                      │                         │                 │
│             │                      │                         │                 │
│             ▼                      ▼                         ▼                 │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                            EventBridge Rules                              │  │
│  └─────────────────────────────────────────┬─────────────────────────────────┘  │
│                                            │                                    │
│                                            │                                    │
│                                            ▼                                    │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                         Automated Response Actions                         │  │
│  │                                                                           │  │
│  │  ┌───────────────────────────┐    ┌─────────────────────────────────────┐ │  │
│  │  │                           │    │                                     │ │  │
│  │  │  Lambda Functions:        │    │  Systems Manager Automation:        │ │  │
│  │  │  - IAM Credential Lockdown│    │  - Security Group Remediation       │ │  │
│  │  │  - S3 Bucket Remediation  │    │  - Host Isolation                   │ │  │
│  │  │  - Alert Routing          │    │  - EC2 Instance Forensics           │ │  │
│  │  │                           │    │                                     │ │  │
│  │  └───────────────┬───────────┘    └───────────────────┬─────────────────┘ │  │
│  │                  │                                    │                   │  │
│  └──────────────────┼────────────────────────────────────┼───────────────────┘  │
│                     │                                    │                      │
│                     │                                    │                      │
│                     ▼                                    ▼                      │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                             Evidence Collection                           │  │
│  │                                                                           │  │
│  │                           S3 Bucket (Encrypted)                           │  │
│  │                                                                           │  │
│  │  ┌───────────────────┐    ┌─────────────────────┐    ┌──────────────────┐ │  │
│  │  │                   │    │                     │    │                  │ │  │
│  │  │  Response Logs    │    │  Forensic Artifacts │    │  Event Timelines │ │  │
│  │  │                   │    │                     │    │                  │ │  │
│  │  └───────────────────┘    └─────────────────────┘    └──────────────────┘ │  │
│  │                                                                           │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Module 4: Incident Response Playbooks

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          Incident Response Playbooks                            │
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                          Incident Response Process                         │  │
│  │                                                                           │  │
│  │  ┌───────────────┐    ┌────────────────┐    ┌────────────────┐    ┌──────┐ │  │
│  │  │               │    │                │    │                │    │      │ │  │
│  │  │  Detection    │───▶│  Analysis      │───▶│  Containment   │───▶│ Eradication│  │
│  │  │               │    │                │    │                │    │      │ │  │
│  │  └───────────────┘    └────────────────┘    └────────────────┘    └──┬───┘ │  │
│  │                                                                      │     │  │
│  │                                                                      │     │  │
│  │                           ┌───────────────┐                          │     │  │
│  │                           │               │                          │     │  │
│  │                           │  Recovery     │◀─────────────────────────┘     │  │
│  │                           │               │                                │  │
│  │                           └───────┬───────┘                                │  │
│  │                                   │                                        │  │
│  │                                   │                                        │  │
│  │                                   ▼                                        │  │
│  │                           ┌───────────────┐                                │  │
│  │                           │               │                                │  │
│  │                           │ Post-Incident │                                │  │
│  │                           │   Review      │                                │  │
│  │                           │               │                                │  │
│  │                           └───────────────┘                                │  │
│  │                                                                           │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                             Playbook Types                                │  │
│  │                                                                           │  │
│  │  ┌───────────────────┐    ┌─────────────────────┐    ┌──────────────────┐ │  │
│  │  │                   │    │                     │    │                  │ │  │
│  │  │  Compromised      │    │  Data Exfiltration  │    │  Malware         │ │  │
│  │  │  Credentials      │    │                     │    │  Response        │ │  │
│  │  │                   │    │                     │    │                  │ │  │
│  │  └───────────────────┘    └─────────────────────┘    └──────────────────┘ │  │
│  │                                                                           │  │
│  │  ┌───────────────────┐    ┌─────────────────────┐    ┌──────────────────┐ │  │
│  │  │                   │    │                     │    │                  │ │  │
│  │  │  DDoS Attack      │    │  Privilege          │    │  General         │ │  │
│  │  │  Response         │    │  Escalation         │    │  Investigation   │ │  │
│  │  │                   │    │                     │    │                  │ │  │
│  │  └───────────────────┘    └─────────────────────┘    └──────────────────┘ │  │
│  │                                                                           │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Module 5: Security Incident Simulations

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          Security Incident Simulations                          │
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                           Simulation Scenarios                            │  │
│  │                                                                           │  │
│  │  ┌───────────────────────────┐          ┌───────────────────────────────┐ │  │
│  │  │                           │          │                               │ │  │
│  │  │  Compromised IAM          │          │  Public S3 Bucket             │ │  │
│  │  │  Credentials Simulation   │          │  Simulation                   │ │  │
│  │  │                           │          │                               │ │  │
│  │  └───────────────┬───────────┘          └─────────────┬─────────────────┘ │  │
│  │                  │                                    │                   │  │
│  │                  │                                    │                   │  │
│  │                  ▼                                    ▼                   │  │
│  │  ┌───────────────────────────────────────────────────────────────────────┐ │  │
│  │  │                                                                       │ │  │
│  │  │                    Automated Response Testing                         │ │  │
│  │  │                                                                       │ │  │
│  │  └───────────────────────────────────────────────────────────────────────┘ │  │
│  │                                                                           │  │
│  │  ┌───────────────────────────────────────────────────────────────────────┐ │  │
│  │  │                                                                       │ │  │
│  │  │                        Tabletop Exercises                             │ │  │
│  │  │                                                                       │ │  │
│  │  │  ┌───────────────────┐    ┌─────────────────────┐    ┌──────────────┐ │ │  │
│  │  │  │                   │    │                     │    │              │ │ │  │
│  │  │  │  Scenario         │    │  Response Team      │    │  Process     │ │ │  │
│  │  │  │  Walkthrough      │    │  Coordination       │    │  Improvement │ │ │  │
│  │  │  │                   │    │                     │    │              │ │ │  │
│  │  │  └───────────────────┘    └─────────────────────┘    └──────────────┘ │ │  │
│  │  │                                                                       │ │  │
│  │  └───────────────────────────────────────────────────────────────────────┘ │  │
│  │                                                                           │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Note on Diagram Usage

These ASCII diagrams are provided for illustrative purposes. In a production environment, you would typically use proper diagramming tools (like draw.io, Lucidchart, or AWS Architecture Diagrams) to create more detailed and visually appealing diagrams. 

The diagrams illustrate the core components and relationships in the security monitoring and incident response solution. As you implement the lab, feel free to customize the architecture to better suit your specific requirements and preferences. 