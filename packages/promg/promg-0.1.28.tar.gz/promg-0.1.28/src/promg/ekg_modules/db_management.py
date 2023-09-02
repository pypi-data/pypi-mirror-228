from typing import List, Set, Optional, Dict


from ..cypher_queries.db_managment_ql import DBManagementQueryLibrary as dbm_ql
from ..data_managers.semantic_header import ConstructedNodes
from ..database_managers.db_connection import DatabaseConnection
from ..utilities.performance_handling import Performance


class DBManagement:
    def __init__(self):
        self.connection = DatabaseConnection()
        self.db_name = self.connection.db_name


    @Performance.track()
    def clear_db(self):
        self.connection.exec_query(dbm_ql.get_clear_db_query, **{"db_name": self.db_name})

    @Performance.track()
    def set_constraints(self):
        # # for implementation only (not required by schema or patterns)
        # self.connection.exec_query(dbm_ql.get_constraint_unique_event_id_query)
        #
        # required by core pattern
        # self.connection.exec_query(dbm_ql.get_constraint_unique_entity_uid_query)
        #
        # self.connection.exec_query(dbm_ql.get_constraint_unique_log_id_query)

        self.connection.exec_query(dbm_ql.get_set_sysid_index_query)

    def get_all_rel_types(self) -> List[str]:
        """
        Find all possible rel types
        @return:
        """

        # execute the query and store the result
        result = self.connection.exec_query(dbm_ql.get_all_rel_types_query)
        # in case there are no rel types, the result is None
        # return in this case an emtpy list
        if result is None:
            return []
        # store the results in a list
        result = [record["rel_type"] for record in result]
        return result

    def get_all_node_labels(self) -> Set[str]:
        """
        Find all possible node labels
        @return: Set of strings
        """

        # execute the query and store the result
        result = self.connection.exec_query(dbm_ql.get_all_node_labels_query)
        # in case there are no labels, return an empty set
        if result is None:
            return set([])
        # some nodes have multiple labels, which are returned as a list of labels
        # therefore we need to flatten the result and take the set
        result = set([record for sublist in result for record in sublist["label"]])
        return result

    def get_statistics(self) -> List[Dict[str, any]]:
        def make_empty_list_if_none(_list: Optional[List[Dict[str, str]]]):
            if _list is not None:
                return _list
            else:
                return []

        node_count = self.connection.exec_query(dbm_ql.get_node_count_query)
        edge_count = self.connection.exec_query(dbm_ql.get_edge_count_query)
        agg_edge_count = self.connection.exec_query(dbm_ql.get_aggregated_edge_count_query)
        result = \
            make_empty_list_if_none(node_count) + \
            make_empty_list_if_none(edge_count) + \
            make_empty_list_if_none(agg_edge_count)
        return result

    def get_event_log(self, entity: ConstructedNodes, additional_event_attributes: List[str]):
        return self.connection.exec_query(dbm_ql.get_event_log_query,
                                          **{"entity": entity,
                                               "additional_event_attributes": additional_event_attributes})

    @Performance.track("query_function")
    def do_custom_query(self, query_function, **kwargs):
        return self.connection.exec_query(query_function, **kwargs)
