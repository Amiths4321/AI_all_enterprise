class ToolPolicy:

    def __init__(
    self,
    planner,
    tools,
    limits,
    tool_policy,
):
    

        self.allowed_tools = (
            allowed_tools
            or {
                "enterprise_retrieval",
            }
        )


    if not tool_policy.can_execute(
          "enterprise_retrieval"
          ):
          state.failure_reason = (
          "tool_not_allowed"
          )
    return state      
    def can_execute(
        self,
        tool_name: str,
    ) -> bool:

        return (
            tool_name
            in self.allowed_tools
        )