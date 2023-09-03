<a id="api"></a>

# API

<a id="module-instrukt.agent"></a>

<a id="instrukt-agent-agents"></a>

## [`instrukt.agent`](#module-instrukt.agent): Agents

Base instrukt agents API

<a id="classes"></a>

### Classes

| [`agent.base.InstruktAgent`](agent/instrukt.agent.base.InstruktAgent.md#instrukt.agent.base.InstruktAgent)                                           | Instrukt agents need to satisfy this base class.                                |
|------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| [`agent.manager.AgentManager`](agent/instrukt.agent.manager.AgentManager.md#instrukt.agent.manager.AgentManager)(ctx)                                | AgentManager handles loading and switching between agents.                      |
| [`agent.state.StateObserver`](agent/instrukt.agent.state.StateObserver.md#instrukt.agent.state.StateObserver)(\*args, \*\*kwargs)                    |                                                                                 |
| [`agent.state.AgentStateSubject`](agent/instrukt.agent.state.AgentStateSubject.md#instrukt.agent.state.AgentStateSubject)()                          |                                                                                 |
| [`agent.state.AgentStateMachine`](agent/instrukt.agent.state.AgentStateMachine.md#instrukt.agent.state.AgentStateMachine)()                          | Agent state machine.                                                            |
| [`agent.loading.ModuleManager`](agent/instrukt.agent.loading.ModuleManager.md#instrukt.agent.loading.ModuleManager)()                                |                                                                                 |
| [`agent.events.AgentEvents`](agent/instrukt.agent.events.AgentEvents.md#instrukt.agent.events.AgentEvents)(value)                                    | An enumeration.                                                                 |
| [`agent.callback.InstruktCallbackHandler`](agent/instrukt.agent.callback.InstruktCallbackHandler.md#instrukt.agent.callback.InstruktCallbackHandler) | Create a new model by parsing and validating input data from keyword arguments. |

<a id="module-instrukt.indexes"></a>

<a id="instrukt-indexes-indexes"></a>

## [`instrukt.indexes`](#module-instrukt.indexes): Indexes

| [`schema.Index`](indexes/instrukt.indexes.schema.Index.md#instrukt.indexes.schema.Index)                                                               | Base Instrukt Index class.                                               |
|--------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| [`schema.Collection`](indexes/instrukt.indexes.schema.Collection.md#instrukt.indexes.schema.Collection)(id, name, metadata)                            | An index collection                                                      |
| [`schema.EmbeddingDetails`](indexes/instrukt.indexes.schema.EmbeddingDetails.md#instrukt.indexes.schema.EmbeddingDetails)(embedding_fn_cls[, ...])     | Details about an embedding                                               |
| [`chroma.ChromaWrapper`](indexes/instrukt.indexes.chroma.ChromaWrapper.md#instrukt.indexes.chroma.ChromaWrapper)(client, collection_name)              | Wrapper around Chroma DB.                                                |
| [`manager.IndexManager`](indexes/instrukt.indexes.manager.IndexManager.md#instrukt.indexes.manager.IndexManager)                                       | Helper to access chroma indexes.                                         |
| [`loaders.AutoDirLoader`](indexes/instrukt.indexes.loaders.SuperDirectoryLoader.md#instrukt.indexes.loaders.AutoDirLoader)(path[, glob, exclude, ...]) | AutoDirLoader is a mix of Langchain's DirectoryLoader and GenericLoader. |

<a id="instrukt-commands-repl-commands"></a>

## [`instrukt.commands`](#module-instrukt.commands): REPL Commands

Instrukt commands.

Commands are created with the Command class and registered using a Route.

RootCmd is the root of all command routes.

# Defining new commands:

To define new commands use the @RootCmd.command decorator.
If you add a command on a separate module, make sure to only export the
decorated functions with \_\_all_\_

| [`command.Command`](commands/instrukt.commands.command.Command.md#instrukt.commands.command.Command)(name, callback, ...)            | A command class representing a command that can be executed in the REPL.   |
|--------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| [`command.CmdGroup`](commands/instrukt.commands.command.CmdGroup.md#instrukt.commands.command.CmdGroup)(name, description[, parent]) | A class representing a group of commands.                                  |
| [`command.CmdLog`](commands/instrukt.commands.command.CmdLog.md#instrukt.commands.command.CmdLog)(msg)                               | Arbitrary log from a command execution.                                    |
