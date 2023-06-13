require "./shares"

module KadaluContentApis
  class Document
    def initialize(@conn : Connection, @path : String)
      @bucket_name = "/"
    end

    def initialize(@conn : Connection, @bucket_name : String, @path : String)
    end

    def self.create(conn, path, obj_type, data, immutable : Bool? = nil, version : Bool? = nil)
    end

    def self.create(conn, bucket_name, path, obj_type, data, immutable : Bool? = nil, version : Bool? = nil)
    end

    def update
    end

    def delete
    end

    def get
    end

    def get_rendered
    end

    def self.list
    end

    def create_share(public : Bool? = nil, password : String? = nil,
                     password_hash : String? = nil, long_url : Bool? = nil,
                     token : String? = nil, token_hash : String? = nil)
    end

    def list_shares
      Share.list(@conn)
    end

    def share(share_id)
      Share.new(@conn, share_id)
    end
  end
end
