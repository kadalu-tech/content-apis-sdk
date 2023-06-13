require "./buckets"
require "./objects"
require "./cnames"

module KadaluContentApis
  class ApiException < Exception
  end

  class Connection
    property username : String?, password : String?, email : String?,
      user_id : String?, token : String?

    # Create a new connection to Kadalu Content APIs
    # If username/email and password provided, then
    # call /api/api-keys and get a token and user_id details.
    # If user_id and token is provided then skip calling the
    # api-keys API.
    #
    # Example:
    #
    # ```
    # conn = KadaluContentApis::Connection.new(
    #   username: "user1",
    #   password: "secret123"
    # )
    # conn = KadaluContentApis::Connection.new(
    #   email: "user1@example.com",
    #   password: "secret123"
    # )
    # ```
    #
    # ```
    # conn = KadaluContentApis::Connection.new(
    #   user_id: 1234,
    #   token: "38969af224e1af005bcdd9fde276d986846416b77c18d39f1d320d1125f01ff2"
    # )
    # ```
    def initialize(@username = nil, @password = nil, @email = nil, @user_id = nil, @token = nil)
      if (!@username.nil? && !@password.nil?) || (!@email.nil? && !@password.nil?)
        # Call the API keys API and save the user_id and token
      end

      if @user_id.nil? || @token.nil?
        raise ApiException.new "invalid arguments"
      end
    end

    # Create a bucket
    def create_bucket(name, region, immutable : Bool? = nil, version : Bool? = nil)
      Bucket.create(self, name, region, immutable: immutable, version: version)
    end

    def list_buckets
      Bucket.list
    end

    def bucket(name)
      Bucket.new(self, name)
    end

    def create_object(path, obj_type, data, immutable : Bool? = nil, version : Bool? = nil)
      Document.create(self, path, data, immutable: immutable, version: version)
    end

    def list_objects
      Document.list
    end

    def object(path)
      Document.new(self, path)
    end

    def create_cname(name)
      Cname.create(self, name)
    end

    def cname(name)
      Cname.new(self, name)
    end

    def create_template(name, tmpl_type, content)
      Template.create(self, name, tmpl_type, content)
    end

    def list_templates
      Template.list
    end

    def template(name)
      Template.new(self, name)
    end
  end
end
