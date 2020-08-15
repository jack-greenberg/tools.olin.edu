const userActions = {
  WHOAMI: "WHOAMI"
}

export function userReducer(state = {}, action) {
  switch(action.type) {
    case userActions.ME:
      return {
        test: null
      }
    default:
      return state;
  }
}
