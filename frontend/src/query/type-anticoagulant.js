const typeAnticoagulant = {
  list() {
    return `query typeAnticoagulantList($limit: Int, $offset: Int, $ordering: String){
        typeanticoagulants(ordering: $ordering) {
            totalCount
            results(limit: $limit, offset: $offset ) {
                id
                name
            }
        }
    }`
  }
}

export default typeAnticoagulant
