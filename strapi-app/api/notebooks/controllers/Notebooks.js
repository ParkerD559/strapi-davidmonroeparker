'use strict';

/**
 * Notebooks.js controller
 *
 * @description: A set of functions called "actions" for managing `Notebooks`.
 */

module.exports = {

  /**
   * Retrieve notebooks records.
   *
   * @return {Object|Array}
   */

  find: async (ctx) => {
    if (ctx.query._q) {
      return strapi.services.notebooks.search(ctx.query);
    } else {
      return strapi.services.notebooks.fetchAll(ctx.query);
    }
  },

  /**
   * Retrieve a notebooks record.
   *
   * @return {Object}
   */

  findOne: async (ctx) => {
    if (!ctx.params._id.match(/^[0-9a-fA-F]{24}$/)) {
      return ctx.notFound();
    }

    return strapi.services.notebooks.fetch(ctx.params);
  },

  /**
   * Count notebooks records.
   *
   * @return {Number}
   */

  count: async (ctx) => {
    return strapi.services.notebooks.count(ctx.query);
  },

  /**
   * Create a/an notebooks record.
   *
   * @return {Object}
   */

  create: async (ctx) => {
    return strapi.services.notebooks.add(ctx.request.body);
  },

  /**
   * Update a/an notebooks record.
   *
   * @return {Object}
   */

  update: async (ctx, next) => {
    return strapi.services.notebooks.edit(ctx.params, ctx.request.body) ;
  },

  /**
   * Destroy a/an notebooks record.
   *
   * @return {Object}
   */

  destroy: async (ctx, next) => {
    return strapi.services.notebooks.remove(ctx.params);
  }
};
