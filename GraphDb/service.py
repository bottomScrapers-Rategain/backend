from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()



class Neo4jConnector:
    def __init__(self, uri, user, password):
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def connect(self):
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))

    def addNode(self, nodeId):
        with self._driver.session() as session:
            session.write_transaction(self._add_node, nodeId)

    def addEdge(self, nodeId1, nodeId2):
        with self._driver.session() as session:
            session.write_transaction(self._add_edge, nodeId1, nodeId2)


    def getConnectedComponent(self, startId, limit=10):
        with self._driver.session() as session:
            result = session.read_transaction(self._get_connected_component_limited, startId, limit)
            return result

    def deleteAllNodesAndEdges(self):
        with self._driver.session() as session:
            session.write_transaction(self._delete_all_nodes_and_edges)

    @staticmethod
    def _add_node(tx, nodeId):
        result = tx.run("MATCH (n:Node {id: $nodeId}) RETURN count(n) AS count", nodeId=nodeId)
        count = result.single()["count"]
        if count == 0:
            tx.run("CREATE (n:Node {id: $nodeId})", nodeId=nodeId)

    @staticmethod
    def _add_edge(tx, nodeId1, nodeId2):
        result = tx.run("MATCH (a:Node {id: $nodeId1})-[:CONNECTED]-(b:Node {id: $nodeId2}) RETURN count(*) AS count",
                    nodeId1=nodeId1, nodeId2=nodeId2)
        count = result.single()["count"]
        if count == 0:
            tx.run("MATCH (a:Node {id: $nodeId1}), (b:Node {id: $nodeId2}) "
                    "CREATE (a)-[:CONNECTED]->(b)", nodeId1=nodeId1, nodeId2=nodeId2)

    @staticmethod
    def _get_connected_component_limited(tx, startId, limit):
        query = (
            "MATCH (start:Node {id: $startId})-[:CONNECTED*1..%d]-(other:Node) "
            "RETURN other.id AS id" % limit
        )
        result = tx.run(query,startId=startId)
        return [record["id"] for record in result]

    @staticmethod
    def _delete_all_nodes_and_edges(tx):
        tx.run("MATCH (n) DETACH DELETE n")

neo4jUri = os.getenv("neo4jUri") 
neo4jUser = os.getenv("neo4jUsername")
neo4jPassword = os.getenv("neo4jPassword")

connector = Neo4jConnector(neo4jUri, neo4jUser, neo4jPassword)
connector.connect()
