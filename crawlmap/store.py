from neo4j.v1 import GraphDatabase


class Store:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def roots(self, urls):
        with self._session() as session:
            session.write_transaction(self._create_roots, urls)

    def pages(self, urls):
        with self._session() as session:
            session.write_transaction(self._create_pages, urls)

    def page_status(self, status):
        with self._session() as session:
            session.write_transaction(self._update_pages, status)

    def links(self, refs):
        with self._session() as session:
            session.write_transaction(self._create_links, refs)

    def leaves(self):
        with self._session() as session:
            return session.read_transaction(self._get_leaves)

    def clear(self):
        with self._session() as session:
            return session.read_transaction(self._clear)

    def _session(self):
        return self._driver.session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._driver.close()

    @staticmethod
    def _create_pages(tx, urls):
        tx.run('UNWIND $urls AS url MERGE (p:Page {url: url}) '
               'SET p.root = EXISTS(p.root) AND p.root, p.used = EXISTS(p.used) AND p.used',
               urls=urls)

    @staticmethod
    def _create_roots(tx, urls):
        tx.run('UNWIND $urls AS url CREATE (p:Page {url: url, root: True, used: False})', urls=urls)

    @staticmethod
    def _update_pages(tx, status):
        tx.run('UNWIND $status AS s MATCH (p:Page {url: s.url}) SET p.code = s.code, p.used = True',
               status=status)

    @staticmethod
    def _create_links(tx, refs):
        tx.run('UNWIND $refs AS ref MATCH (a:Page {url: ref.from}), (b:Page {url: ref.to}) '
               'CREATE (a)-[:REFERENCES]->(b)',
               refs=refs)

    @staticmethod
    def _get_leaves(tx):
        return [r['p.url'] for r in tx.run('MATCH (p:Page {used: False}) RETURN p.url')]

    @staticmethod
    def _clear(tx):
        tx.run('MATCH (a)-[b]->(c) DELETE a, b, c')
        tx.run('MATCH (a) DELETE a')
