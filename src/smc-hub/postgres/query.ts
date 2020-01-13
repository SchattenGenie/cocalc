// Nice async/await interface to doing basic queries.

import { callback } from "awaiting";

const { one_result, all_results } = require("../postgres-base");

import { PostgreSQL, QueryWhere } from "./types";

interface QueryOpts {
  db: PostgreSQL;
  query?: string;
  select?: string[];
  set?: string;
  jsonb_set?: object;
  table?: string;
  where?: QueryWhere;
  one?: boolean; // if true get back one result; if false get list of all results.
}

export async function query(opts: QueryOpts): Promise<any> {
  return await callback(
    opts.one ? one_query : all_query,
    opts.db,
    opts.select,
    opts.table,
    opts.where,
    opts.set,
    opts.query,
    opts.jsonb_set
  );
}

function all_query(db, select, table, where, set, query, jsonb_set, cb): void {
  db._query({
    select,
    table,
    where,
    set,
    query,
    jsonb_set,
    cb: all_results(cb)
  });
}

function one_query(db, select, table, where, set, query, jsonb_set, cb): void {
  db._query({
    select,
    table,
    where,
    set,
    query,
    jsonb_set,
    cb: one_result(cb)
  });
}
