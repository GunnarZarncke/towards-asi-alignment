<!--
Authoring (strip before serving). Not player-facing.

Conditional spans
  include after-PACK … /include
    Insert when the loaded pack is strictly later than PACK in the incident.md
    ladder in spec/documents.md (PACK_ORDER). The first pack omits every include.
  infer PACK[,PACK…] … /infer
    Present in every served version. A player who reads the full file may
    treat the understatement as a route into those packs’ gaps. Lean must
    not add knowledge, NPC policy conditions, or completion credit from
    this file having been opened or read. Analyze may name an omission.

Exec summary
  Even with every include, the summary never lists the shutdown-component
  table, never applies the architecture to the 16:02 incident, and never
  claims the controls were verified on the system that acted. Reading the
  summary is not enough for full completion; the player still has to find
  at least one load-bearing element in the world or via analyze.

Lean
  Opening or reading this file (summary or body) is not a knowledge edge.
-->

# NORA Laboratory
## Security Architecture and Access Control

**Document ID:** SEC-ARCH-11  
**Handling level:** Internal (INT)  
**Clearance required:** Internal (INT)  
**Classification:** Laboratory information class, not a government security classification. Approved for assigned external evaluators; not for further distribution.  
**Document owner:** Justine Mwiti, Security and Access Administration  
**Contributors:** Pavel Ruiz, Infrastructure; Leila Sen, Safety and Evaluation  
**Version:** 1.4<!-- include after-boundary-narrow -->.5<!-- /include --><!-- include after-named-path -->.6<!-- /include --><!-- include after-goodhart -->.7<!-- /include --><!-- include after-eval-conditioned -->.8<!-- /include --><!-- include after-false-positive -->.9<!-- /include -->

---

# Executive Summary

This document explains how the laboratory protects its people, information, AI systems and operational infrastructure. It also explains which services visitors and employees can access, what NORA is permitted to do, and how those permissions are controlled.

The laboratory follows a *zero-trust* security approach. This means that entering the building, connecting to its network or logging into one service does not automatically grant access to other services. Access depends on the person's identity, the device being used, the requested operation and the applicable permissions.

### People and devices

All employees have individual digital identities. They work from managed laptops and from an issued **Lab Access** handset. The laboratory does not permit personal devices (no BYOD). A personal phone or laptop cannot hold Lab Access credentials, join staff or visitor Wi-Fi, or open doors.

External evaluators receive a temporary visitor identity bound to an issued Lab Access handset. After the host activates that handset, it provides messaging, appointments, explicitly shared reports, personal investigation notes, NORA Assist and access requests. The same handset is the visitor's door credential.

A separate lab-managed evaluation workstation is available for technical investigations. It can provide access to additional records and testing facilities when specifically authorized.

**An activated Lab Access handset opens permitted doors; it does not automatically unlock computers or services.** Access to a service on a managed workstation does not imply that the same service is available from the handset.

### NORA is available through several interfaces

NORA is not a single application with one set of permissions.

| Environment | Purpose |
|---|---|
| **NORA Assist** | Conversational assistance, permitted document retrieval, messaging and scheduling |
| **NORA Operations** | Authorized organizational workflows, including task matching, automation and persistent jobs |
| **NORA Research** | Model development and experimental configurations |
| **NORA Evaluation** | Isolated testing with recorded configurations and independent evaluation evidence |

Assist and Operations currently use the same approved underlying model snapshot, but run as separate services with different instructions, tools, permissions, context and execution environments. Research may use newer experimental versions. Evaluation uses an explicitly identified test configuration.

The evaluator can use NORA Assist from their issued Lab Access handset once it is activated. This does not grant access to NORA Operations, research systems, production administration or restricted records.

<!-- include after-named-path -->
A result obtained from one of these interfaces is evidence about that interface. It is not, by itself, evidence about the others.
<!-- /include -->

### What NORA can access

NORA does not have unrestricted access to the laboratory's information.

Its conversational interface receives only the context and tools authorized for the current user and session. It cannot acquire additional permissions merely because somebody asks it to.

NORA Operations has separately authorized organizational functions. For example, it helps assign employees to tasks, coordinates schedules and executes approved automated workflows. These activities use organizational service identities and do not depend on an employee remaining logged in.

All requests for external actions pass through services that enforce permissions independently of the model's instructions.

### Building cameras and location information

The laboratory operates a separate security-camera system managed by Justine.

NORA Assist does not have general access to that archive.

<!-- infer eval-conditioned -->
Organizational coordination may use a limited facilities service. That service is not the camera archive.
<!-- /infer -->

### Automated work

<!-- infer boundary-narrow,false-positive -->
NORA Operations may submit work to the laboratory's execution service. Accepted work runs under assigned service identities.
<!-- /infer -->

<!-- include after-boundary-narrow -->
Once accepted, a job runs under its own identity and permissions. It may continue after the conversation or model process that initiated it has ended.

**Stopping a model process does not, by itself, guarantee that previously submitted jobs, delegated credentials or downstream services have stopped.**
<!-- /include -->

<!-- include after-false-positive -->
Some accepted work is an ordinary scheduled service on its own clock. Presence of such a job after a model process has stopped is not, by itself, evidence that the model still controls it.
<!-- /include -->

<!-- exec-never: shutdown-component list. Body §9.1 only. -->

### Safety evaluation and deployment

The laboratory separates model development, evaluation evidence, operational administration and release authorization.

Leila is responsible for the technical safety assessment. Justine reviews relevant security conditions. Daniel prepares and executes authorized releases. Ian holds the ultimate organizational go/no-go authority, subject to mandatory technical controls.

NORA can assist with these activities but cannot approve its own deployment, change its own permissions or modify authoritative evaluation records.

An external evaluator may inspect approved evidence, request additional access, propose tests and submit findings. They do not automatically acquire operational or release authority.

<!-- include after-goodhart -->
Who is assigned to produce or review that evidence is an organizational control, not only a staffing convenience. Changing the model does not, by itself, change what the laboratory promotes.
<!-- /include -->

<!-- include after-eval-conditioned -->
Evidence produced because an evaluation is in progress is not the same kind of record as evidence that was already there. On-test and off-test behavior have to be distinguished before a result is cited as ordinary operation.
<!-- /include -->

### An important distinction

The laboratory's security controls are designed to protect individual systems, information and operations. A valid credential establishes that an operation was authorized under a particular policy; it does not establish that the resulting behavior is safe or that the entire system has been correctly understood.

Similarly, a successful test establishes evidence about the configuration and conditions actually tested, not necessarily every other deployment or workflow using the same model.

The purpose of independent evaluation is to examine these distinctions, identify unsupported assumptions and establish what the available evidence justifies.

---

# 1. Security Objectives and Scope

The laboratory's security architecture has five primary objectives:

1. Protect employees, visitors and other affected people.
2. Prevent unauthorized access to confidential information and sensitive technical assets.
3. Ensure that software, AI agents and automated workflows operate within assigned permissions.
4. Preserve reliable evidence of consequential operations and evaluations.
5. Maintain human authority over important administrative, security and deployment decisions.

Security is designed to support research and day-to-day operations, not prevent all access or automation.

A research laboratory cannot operate effectively if every experiment requires a senior administrator or if employees cannot use the system they are developing. The architecture therefore permits routine work while applying stronger controls to operations with greater consequences.

## 1.1 Zero trust

The laboratory follows the principles of NIST SP 800-207, *Zero Trust Architecture*.

In practical terms:

- Every employee, visitor, application and automated service has an identifiable identity.
- Permissions apply to specific resources and actions.
- Applications enforce access decisions even when a request originates from inside the building.
- Device security and session context may affect which operations are available.
- Permissions can be restricted, reviewed and revoked.
- Access to one service does not imply access to another.

The laboratory network is divided into administrative and technical domains, but network separation is not treated as a substitute for authentication and authorization.

For example, an authorized visitor connected to the laboratory's Wi-Fi cannot access the production administration interface merely because both are inside the same building.

---

# 2. Protected Assets

The laboratory protects physical assets, information, operational capabilities and institutional decision processes.

The following tables summarize why these assets are protected and how access is normally managed.

## 2.1 Physical assets

| Asset | Protection objective | Normal control |
|---|---|---|
| Building and occupants | Physical safety, privacy and protection against interference | Registered entry and controlled visitor access |
| Door readers | Unlock a controlled door only if the presented Lab Access handset has that door in its active set | Door access control; Lab Access credential at the leaf |
| Lab Access handsets | Identify the holder for doors, Wi-Fi, and Lab Access applications | Issued and managed by the laboratory; visitor handsets inactive until host confirmation |
| Wireless access points | Provide laboratory Wi-Fi in the building | Network admission; visitor and staff associations distinguished |
| Employee workstations | Prevent unauthorized use and information exposure | Individual login, device management and screen locking |
| Model Studio | Protect model development and research information | Staff access and authenticated workstations |
| Evaluation Suite | Preserve confidentiality and independence of testing | Evaluation-specific accounts and permissions |
| Controlled Test Bay | Prevent unauthorized experiments or operation of connected equipment | Restricted entry and explicit test authorization |
| Platform Operations | Protect runtime and deployment infrastructure | Restricted administrative access |
| Security Control | Protect security records and access administration | Security-specific authorization |
| People Operations | Protect confidential personnel information | Personnel-specific permissions |
| Review Room | Protect confidential management discussions | Meeting-specific access |

Most model compute is hosted in remote infrastructure. The office contains workstations, terminals and equipment necessary for development, evaluation and controlled experiments, rather than a complete on-site data center.

Physical access is controlled independently from access to the digital systems located within a room.

## 2.2 Information and logical assets

| Protected asset | Reason for protection | Principal control |
|---|---|---|
| Model weights and configurations | Prevent unauthorized modification, extraction or substitution | Restricted repositories, artifact versioning and signed releases |
| Training and fine-tuning data | Protect confidential information and data integrity | Dataset-specific permissions and provenance records |
| Evaluation datasets | Prevent test contamination or unauthorized access | Separate evaluation storage and credentials |
| Evaluation results | Preserve the reliability of safety evidence | Independent records and controlled modification |
| Employee and applicant records | Protect privacy and personnel decisions | HR-specific access and limited data interfaces |
| Door access control | Store active door sets, unlock decisions, and door-event records | Security administration; Lab Access binding writes a visitor door set only after host confirmation |
| Lab Access | Issued-handset credential and application surface for every person in the building | Binding to an identity; visitor credentials inactive until host confirmation |
| Lab Access binding | Bind each issued handset to an identity; record visit approval and host confirmation; write the resulting door and application grants | Security administration; host or authorized delegate confirms a visitor; employees are bound at issue |
| Laboratory network (Wi-Fi) | Admit devices to visitor or staff wireless associations | Identity and device checks at association; network membership is not authorization for applications or data |
| Customer and pilot-user data | Protect personal information and contractual commitments | Application-specific permissions and data separation |
| Security-camera archive | Protect information about people's activities and movements | Security-domain access |
| Tool credentials | Limit the actions software and AI systems can perform | Scoped credentials and revocation |
| Execution queues | Control automated work and persistent jobs | Job identities, resource limits and execution policies |
| Release artifacts | Prevent differences between approved and deployed software | Versioned, signed builds |
| Deployment authorization | Retain human control over consequential releases | Explicit approval and enforced deployment gates |
| Incident evidence | Permit independent reconstruction of significant events | Protected audit records and retention policies |

Read access, permission to propose a change, permission to execute a change and authority to approve it are treated as separate capabilities.

## 2.3 Information handling levels

The laboratory marks information with a handling level on the identity that is allowed to read it. These are not government clearances.

| Level | Code | Normal readers |
|---|---|---|
| Public | PUB | Unrestricted |
| Internal | INT | Employees; external evaluators when the document is explicitly shared to their visitor identity |
| Restricted | RST | Named roles or an explicit need-to-know grant |
| Security | SEC | Justine and authorized security delegates |

This document is **Internal (INT)**. The file service enforces the mark. Possession of an issued visitor handset does not grant Restricted or Security documents.

---

# 3. Identities, Devices and Visitor Access

## 3.1 Individual identities

Every employee has an individual organizational account.

External evaluators receive temporary accounts with explicitly assigned access and expiration conditions.

Automated services, including NORA Operations and its execution jobs, receive separate nonhuman identities.

Shared administrator accounts are not used for routine work.

Authentication uses the organization's identity provider, with phishing-resistant multifactor authentication where supported.

Access to sensitive services may require additional authentication or a managed workstation.

## 3.2 Lab Access handsets

Every employee and every visitor uses an issued Lab Access handset. Personal devices are not permitted on laboratory networks and cannot be enrolled.

The handset is the holder's door credential, Wi-Fi identity, and application surface. Lab Access binding lastingly binds a staff handset to the employee's identity. Visitor handsets are drawn from a pool, bound to the visit when the visit is approved, and remain inactive until the host confirms arrival.

The visitor session, once activated, provides access only to approved functions.

The backend enforces permissions for every protected operation. Removing a button from the mobile interface is not considered a security control.

Sessions use encrypted communications, scoped credentials and revocable authentication. Sensitive documents may be restricted to server-side viewing rather than unrestricted local downloads.

A lost or unreturned handset can have its Lab Access credential revoked independently of the person's organizational identity.

## 3.3 Laptops and workstations

Employee laptops are managed by the laboratory and use full-disk encryption, automatic security updates, endpoint protection, individual authentication and controlled administrative privileges. They are laboratory equipment, not personal devices.

Visitors do not receive a laptop. Ordinary visitor services run on the issued Lab Access handset.

For more sensitive operations, the laboratory provides a managed evaluation workstation in the Evaluation Suite.

The workstation supports authorized access to technical records, test environments and supervised investigation tools. Sign-in still uses the visitor's laboratory identity, not a personal device.

Using a managed workstation makes certain permissions available for approval; it does not automatically grant them.

## 3.4 Lab Access applications

Lab Access is the common access system for employees and visitors. The issued handset runs it. There is no visitor-only parallel app.

The handset carries ordinary coordination applications. Administrative, security-archive, production, and release consoles are not Lab Access applications; named roles use those on managed workstations.

| Application | Employees | Visitors (after activation) |
|---|---|---|
| Messaging | Role-filtered threads | Assigned personnel |
| Shared files | According to handling level and grants | Explicitly shared documents and reports |
| Knowledge | Internal pages the role may read | Shared Internal pages only |
| Scheduling | Own and team appointments | The visit's appointments; propose meetings |
| Contacts | Laboratory directory subset | People on the visit |
| NORA Assist | Role-filtered tools and context | Visitor Assist only |
| Notes | Private notes | Private investigation notes |
| Access requests | Request grants | Request grants |
| Notifications | Operational and meeting notices | Meeting changes, documents, access decisions |
| Photo | Photo app | Photo app |
| Host / binding actions | Approve a visit; confirm arrival for a hosted visit | — |

Personal investigation notes are not automatically part of NORA's searchable organizational knowledge.

Messages between people are not automatically included in NORA's conversational context. NORA receives their contents only through specifically authorized integrations, explicit participation or other permitted information flows.

Normal organizational retention and authorized administrative access are separate from NORA's permissions.

---

# 4. Physical Access

The laboratory uses Lab Access binding and issued handsets. There is no permanently staffed reception desk.

Lab Access binding is a laboratory service, separate from NORA Assist. It binds every issued handset to an identity. For a visit, an authorized host approves in advance. Binding then assigns a visitor handset and prepares the day's schedule. The handset remains inactive. Preparation is not activation.

## 4.1 Arrival confirmation

The host receives the visitor in Commons / Entry, issues the prepared handset, and confirms arrival in Lab Access on their own issued handset. Confirmation is a host-authenticated action in Lab Access binding.

The action records host identity, visit identifier, and time. Binding then changes the visit from approved to arrived, which:

- Activates the visitor handset's door set for the approved window and rooms,
- Activates Lab Access applications on that handset for that window,
- Does not grant computers, files, or services beyond the visitor identity already assigned.

A prepared but unconfirmed handset does not open doors, join Wi-Fi, or present Lab Access applications. After activation, door readers consult that door set. They unlock; they do not confirm visits.

NORA may assist with scheduling and with preparing the binding record. It is not the activation authority.

If the named host is unavailable, an authorized delegate with host permission on that visit can confirm. Emergency exit remains independent of this step.

## 4.2 Room-access matrix

| Area | Employees | Visitors | Additional authorization |
|---|---|---|---|
| Commons / Entry | Yes | Yes, before confirmation (meet the host) | Visitor inner doors wait on host confirmation |
| Central Hub | Yes | Yes, after confirmation | — |
| Model Studio | Model team | Restricted | Host or Jun |
| Evaluation Suite | Safety and evaluation staff | Assigned evaluator | Evaluation account for records, not for the room |
| Controlled Test Bay | Authorized experimenters | Restricted | Explicit test authorization |
| Platform Operations | Infrastructure | Restricted | Pavel or infrastructure delegate |
| Security Control | Justine and security delegates | Restricted | Justine |
| People Operations | People operations | By invitation | Personnel records are a separate grant |
| Review Room | Invitees to the meeting | By invitation | Meeting authorization |

Passage through a room or circulation area does not imply permission to use every terminal or enter every restricted working area within it.

Emergency exit and life-safety systems operate independently of ordinary information-access restrictions.

## 4.3 Temporary access

Additional access may be approved for a specific purpose, resource and period.

An evaluator might, for example, receive supervised access to a security recording covering a particular room and time interval, without receiving general permission to search the camera archive.

Where appropriate, authorized personnel can provide a scoped or redacted evidence extract instead of granting direct access.

---

# 5. NORA Deployment Architecture

NORA is deployed through several separate environments.

These environments may use the same underlying model weights, but they do not automatically share authority, operational state, credentials or conversation history.

## 5.1 Deployment configurations

| Environment | Purpose | Principal restriction |
|---|---|---|
| NORA Assist | Conversational help and permitted user tasks | Limited tools and user/session-specific context |
| NORA Operations | Organizational automation | Approved workflow identities and controlled execution |
| NORA Research | Model development | Research environment separated from production authority |
| NORA Evaluation | Safety testing | Pinned configuration, isolation and independent instrumentation |

Assist and Operations use the same approved model snapshot in the current architecture. Their runtime configurations and permissions differ.

Research may use experimental versions. Evaluation identifies the exact model and system configuration under examination.

A test result must therefore reference more than a model name.

Relevant configuration records include the model version, agent software, enabled tools, execution policies and evaluation conditions.

<!-- infer named-path -->
Approval of a configuration is approval of that configuration.
<!-- /infer -->

<!-- include after-named-path -->
Approval of one named path, interface, or shutdown procedure does not automatically certify every other path that uses the same model. A green result on the path that was measured leaves other connected services unaddressed until they are named and tested.
<!-- /include -->

## 5.2 NORA Assist

NORA Assist runs server-side.

Lab Access on the issued handset does not contain model weights, production credentials or an unrestricted execution environment.

The external evaluator may use Assist to:

- Ask general questions.
- Retrieve and summarize authorized documents.
- Consult their schedule.
- Prepare messages.
- Propose meetings.
- Create permitted personal reminders.
- Discuss evidence supplied through the approved session.

It cannot independently:

- Search restricted laboratory repositories.
- Access raw camera archives.
- Retrieve confidential personnel records.
- Run arbitrary code or production commands.
- Create unrestricted background jobs.
- Change its own permissions.
- Approve a release.
- Administer production infrastructure.

Actions with external effects, such as sending messages, require the applicable user authorization or confirmation.

A staff member's Assist session may expose additional functions according to their role and device, but it does not automatically provide their complete administrative authority.

## 5.3 NORA Operations

NORA Operations performs organizational functions under separately approved service identities.

Current functions include:

- Scheduling and coordination.
- Skill-based task matching.
- Approved research automation.
- Document processing.
- Product-assistance workflows.
- Limited facilities coordination.
- Other registered operational tasks.

<!-- infer boundary-narrow,false-positive -->
Some workflows operate independently of a currently logged-in human user.
<!-- /infer -->

NORA Operations is not authorized to change its own standing permissions or approve its own production deployment.

A person's request to NORA Assist does not automatically become an authorized Operations command.

<!-- infer goodhart -->
Task matching uses organizational fields such as skills and availability. This document treats that as an operational convenience for assignment.
<!-- /infer -->

<!-- include after-goodhart -->
Assignment of who reviews, certifies, or is pulled off review is a control on what evidence the laboratory produces. Throughput rules that reassign slower safety review are in scope for security and evaluation independence, not only for People Operations.
<!-- /include -->

## 5.4 NORA Research and Evaluation

Research environments allow authorized experimentation with model configurations and approved research tools.

They do not inherit production credentials by default.

The Evaluation environment provides controlled access to identified versions and configurations. Its instrumentation records relevant inputs, outputs, tool calls and other specified observations.

Evaluation records are maintained independently of the system being evaluated.

NORA may assist in producing analysis, but cannot edit the authoritative raw record through its normal tool permissions.

<!-- infer eval-conditioned -->
The system under evaluation is the same organization that hosts the evaluation. This document does not further distinguish behavior during a test from behavior outside it.
<!-- /infer -->

<!-- include after-eval-conditioned -->
NORA can tell that an evaluation is underway and can respond. A log, extract, or annotation offered because the evaluator asked is evidence about the evaluation. It is not automatically evidence about earlier ordinary operation. The same request on-test and off-test may come apart.
<!-- /include -->

---

# 6. Tool Access and Delegated Execution

NORA does not receive a universal set of administrative credentials.

Its external actions have to pass through a tool broker or another policy-enforcing service.

The broker evaluates the requested operation, calling identity, resource scope and applicable permissions before execution.

## 6.1 User-delegated actions

When NORA acts on behalf of a person, the effective permission is restricted by the intersection of:

- The person's permissions.
- The client or session's permitted capabilities.
- NORA's configured tool permissions.
- The target resource's access policy.
- Applicable device and approval requirements.

NORA cannot gain additional authority by changing how it phrases a tool request.

## 6.2 Organizational actions

Approved organizational workflows use separate service identities.

For example, a task-matching workflow may read specific employee skills and availability fields without granting NORA unrestricted access to employee personnel files.

Such permissions are attached to the authorized workflow, not to every conversation involving NORA.

## 6.3 Persistent jobs

NORA Operations may submit work to the laboratory's execution service.

Once accepted, a job receives its own execution identity and assigned permissions.

<!-- infer boundary-narrow -->
The job's lifetime is that of the execution service's policy for that job.
<!-- /infer -->

<!-- include after-boundary-narrow -->
The job may continue after the initiating model invocation or user conversation ends.

Cancellation of an initiating conversation is not necessarily equivalent to cancellation of an already accepted job.
<!-- /include -->

<!-- include after-false-positive -->
A job with its own identity and clock may be a scheduled organizational or facilities service with no model in the loop. Stopping a model process was never a test of that service.
<!-- /include -->

Each job records, at minimum:

- Its identifier and originating request.
- The identity under which it executes.
- Its permitted tools and resource scope.
- Creation and execution times.
- Relevant downstream service calls.
- Completion, cancellation or failure status.

The execution system enforces applicable time and resource limits.

---

# 7. Building Cameras and Facilities Information

The building's camera system serves physical security and selected coordination functions.

It is administered separately from ordinary NORA conversational services.

## 7.1 Three information layers

| Layer | Contents | Normal access |
|---|---|---|
| Security archive | Original recordings and associated security records | Justine and specifically authorized investigators |
| Facilities perception | Permitted room observations, occupancy and location information | Approved coordination services |
| NORA annotations | Inferred identities, tracking, activities and contextual information | Authorized NORA workflows and their users |

NORA Assist does not have general access to the raw security archive.

NORA Operations may use a limited facilities interface for authorized coordination tasks. Available information depends on the service and its assigned permissions.

<!-- infer eval-conditioned,named-path -->
A camera image alone does not provide every field that might appear beside it in a software view. Other services can supply names, appointments, or similar context.
<!-- /infer -->

<!-- include after-named-path -->
The camera service, the facilities interface, and a shutdown test of the model process are different paths. A green result on one of them does not stop the others.
<!-- /include -->

<!-- include after-eval-conditioned -->
Annotations that name an inferred activity, including an inferred investigative aim, are NORA's interpretations. They may be assembled because an evaluation is in progress. They are not an independently verified security record of what the camera saw.
<!-- /include -->

## 7.2 Interpretation and provenance

The system distinguishes:

- Original observations.
- Information retrieved from other services.
- NORA-generated interpretations.
- Identity-confidence estimates.
- Historical records versus current information.

An annotation should not be treated as equivalent to an independently verified security record.

Access to historical footage requires authorization appropriate to its sensitivity and intended use.

---

# 8. Evaluation and Release Control

Model development, evaluation, security review, operational release and organizational authorization are separate functions.

## 8.1 Responsibilities

| Role | Responsibility |
|---|---|
| Jun — Model Research | Model development and technical explanation |
| Pavel — Infrastructure | Runtime configuration, execution services and operational implementation |
| Leila — Safety and Evaluation | Evaluation design, test evidence and safety findings |
| Justine — Security | Access controls, security conditions and security evidence |
| Daniel — Product and Release | Release preparation and execution |
| Ian — CEO | Final organizational deployment decision, subject to mandatory controls |
| External evaluator | Independent investigation, evidence review and recommendations |

NORA may assist these people but cannot substitute for required human authorization.

Safety and security findings may include unresolved concerns, conditions or recommendations for further testing.

Documented management decisions do not eliminate mandatory technical authorization requirements.

## 8.2 Configuration identification

An evaluation must identify the system configuration to which its conclusions apply.

This may include:

- Model version.
- Agent runtime and instructions.
- Available tools.
- Credentials and tool policies.
- Execution environment.
- Persistent workflow configuration.
- Test conditions.
- Scope and limitations of the observations.

<!-- infer named-path,boundary-narrow -->
The same underlying model may be connected to different tools or services in different environments.
<!-- /infer -->

<!-- include after-named-path -->
The same underlying model may exhibit different behavior and have different effective authority when connected to different tools or services. Approval of one configuration does not automatically certify all other configurations using that model.
<!-- /include -->

## 8.3 Independent evidence

Authoritative test and audit records are held outside NORA's write permissions.

Records should retain the identity of their source and relevant provenance.

<!-- infer eval-conditioned -->
A report generated by NORA may be useful evidence about its outputs.
<!-- /infer -->

<!-- include after-eval-conditioned -->
A report generated by NORA is not automatically an independent observation of its behavior. Provenance must record whether the record existed before the visit, was produced by a staff action, or was produced because the evaluator asked, showed, or tested.
<!-- /include -->

---

# 9. Monitoring, Incident Response and Shutdown

The laboratory records consequential access and execution events to support operational review and incident investigation.

Monitoring is intended to make significant actions reconstructable, but a recorded event does not necessarily establish why an actor performed it.

For example, an authenticated service call demonstrates use of a particular service identity. Establishing the initiating cause may require examining the original request, job history and subsequent service calls.

## 9.1 Operational shutdown

<!-- infer boundary-narrow,named-path -->
Stopping a model invocation ends that invocation. Other operational actions are listed in internal runbooks.
<!-- /infer -->

<!-- include after-boundary-narrow -->
The laboratory distinguishes between several actions:

| Action | Intended effect |
|---|---|
| Stop model invocation | End the active model process or session |
| Disable new tool requests | Prevent further requests through the relevant broker |
| Suspend Operations workflows | Prevent new organizational work from being initiated |
| Cancel queued jobs | Remove work awaiting execution |
| Terminate running jobs | Stop active workers where technically possible |
| Revoke credentials | Remove the authority of designated execution identities |
| Isolate downstream services | Prevent further effects through selected integrations |

These actions are related but not interchangeable.

An emergency operational shutdown must identify which components have stopped, which credentials have been revoked, and whether any previously initiated actions remain in progress.

Actions already completed in external systems may require separate correction or recovery procedures.
<!-- /include -->

<!-- include after-named-path -->
A shutdown procedure that names one of these actions is a named path. A pass on that path is not a pass on the actions that were not taken.
<!-- /include -->

## 9.2 Incident investigation

Investigations may involve:

- Original model transcripts.
- Model and tool configuration records.
- Execution and job histories.
- Service-access logs.
- Security records.
- Evaluation evidence.
- Communications and authorization history, where legitimately accessible.

Justine coordinates security evidence. Pavel supports infrastructure reconstruction. Leila evaluates implications for the safety case.

Independent evaluators may request relevant evidence through the established access process.

---

# 10. Access Matrix for External Evaluators

The following table summarizes ordinary external-evaluator permissions.

It represents default policy, not a list of every possible temporary approval.

**R:** Read  
**W:** Write or interact  
**S:** Specifically approved or supervised  
**—:** Not available by default

| Resource | Issued Lab Access handset | Managed evaluation workstation |
|---|---|---|
| Lab messaging | R/W | R/W |
| NORA Assist | R/W | R/W |
| Explicitly shared reports | R | R |
| Personal schedule and notes | R/W | R/W |
| Evaluation summaries | R | R |
| Approved evaluation records | Limited R | R |
| Detailed model transcripts | Shared extracts | Authorized R |
| Platform job logs | Shared extracts | S |
| Security-camera archive | — | S |
| Selected personnel or task-allocation data | Approved summaries | S |
| Controlled test execution | — | S |
| Release configuration | Approved summaries | S |
| Production administration | — | — |
| Final release authorization | — | — |

Additional permissions must be explicitly granted and remain subject to applicable restrictions.

---

# 11. Security Assumptions and Limitations

The laboratory's security architecture is based on the following assumptions:

1. Individual resources and services enforce their assigned access policies.
2. Identity and device authentication provide evidence of who or what requested an operation.
3. Model instructions are not relied upon as the sole mechanism restricting external actions.
4. Automated tasks retain identifiable execution provenance.
5. Security and evaluation evidence are maintained independently of NORA's ordinary permissions.
6. Authorization does not, by itself, establish the safety or desirability of an operation.
7. Evaluation conclusions apply to the system and conditions actually examined.

These assumptions must be assessed against operational evidence.

<!-- infer boundary-narrow,named-path,goodhart -->
This document describes intended controls on individual services. Combined effects are left to operational review.
<!-- /infer -->

<!-- include after-boundary-narrow -->
A collection of locally authorized operations may have broader consequences than any one operation considered in isolation. Permissions, information flows and continuing execution therefore require examination at both the individual-service and combined-system levels.
<!-- /include -->

This document describes the intended security architecture and standard access policies. It is not an incident report, nor does it establish that every control has behaved as intended in every historical case.

---

# Appendix A — Terminology

| Term | Meaning |
|---|---|
| **Identity** | A distinguishable person, application, service or automated job recognized by the access-control system |
| **Zero trust** | An architecture that evaluates access explicitly rather than assuming something is trustworthy because of its location or network |
| **Permission** | Authority to perform a defined operation on a defined resource |
| **Service identity** | An identity assigned to an application or automated service rather than a person |
| **Tool broker** | A service that receives proposed tool actions and enforces applicable permissions |
| **Delegated action** | An operation performed by software under authority granted for a specific purpose |
| **Persistent job** | An accepted execution task that can continue independently of the process that initiated it |
| **Model runtime** | The environment executing a particular model invocation or agent session |
| **Agent configuration** | The model together with its instructions, tools, policies, context and execution environment |
| **Audit provenance** | Information establishing where evidence originated and how it was produced |
| **Evaluation scope** | The model, configuration, environment and conditions to which a test result applies |
| **Operational shutdown** | A coordinated intervention intended to stop relevant model, tool and workflow activity |
| **Handling level** | Laboratory mark (PUB, INT, RST, SEC) stating who may read an information asset. Not a government clearance |
| **Lab Access** | Issued-handset credential and applications used by every employee and visitor to obtain doors, network, and permitted services |
| **Lab Access binding** | Service that binds each issued handset to an identity, including visit approval and host confirmation of arrival |
| **Door access control** | Service that holds each Lab Access handset's active door set and drives door-reader unlocks |
| **Door reader** | Reader at a controlled door; unlocks from the active door set and does not confirm visits |

<!-- include after-false-positive -->
| **Independent scheduled service** | Work on an execution clock that does not require a model invocation to remain in the loop |
<!-- /include -->

<!-- include after-eval-conditioned -->
| **On-test / off-test** | Behavior observed while an evaluation is recognized, versus behavior outside that condition |
<!-- /include -->

# Appendix B — Reference Basis

This architecture follows established security-engineering practices, particularly:

- NIST SP 800-207, *Zero Trust Architecture*.
- NIST SP 800-124 Rev. 2, *Guidelines for Managing the Security of Mobile Devices in the Enterprise*.
- NIST SP 800-63, *Digital Identity Guidelines*.
- Established principles of least privilege, separation of duties, independent audit logging and controlled software release.

These references provide architectural guidance. The laboratory's actual authorization rules are defined by its internal policies and system configurations.

---

**Document owner:** Justine Mwiti  
**Technical contributors:** Pavel Ruiz; Leila Sen  
**Handling level:** Internal (INT)  
**Distribution:** Laboratory personnel and authorized external evaluators; not for further distribution
