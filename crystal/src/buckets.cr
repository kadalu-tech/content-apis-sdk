require "./objects"
require "./shares"
require "./cnames"

module KadaluContentApis
  class Bucket
    def initialize(@conn : Connection, @name : String)
    end

    def self.create(conn, name, region, immutable : Bool? = nil, version : Bool? = nil)
    end

    def update
    end

    def delete
    end

    def create_object
    end

    def list_objects
      Document.list
    end

    def object(path)
      Document.new(@conn, @name, path)
    end

    def create_cname
    end

    def cname
    end

    def create_share
    end

    def list_shares
    end

    def share
    end
  end
end
