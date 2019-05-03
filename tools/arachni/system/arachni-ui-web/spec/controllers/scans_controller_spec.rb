require 'spec_helper'

# This spec was generated by rspec-rails when you ran the scaffold generator.
# It demonstrates how one might use RSpec to specify the controller code that
# was generated by Rails when you ran the scaffold generator.
#
# It assumes that the implementation code is generated by the rails scaffold
# generator.  If you are using any extension libraries to generate different
# controller code, this generated spec may or may not pass.
#
# It only uses APIs available in rails and/or rspec-rails.  There are a number
# of tools you can use to make these specs even more expressive, but we're
# sticking to rails and rspec-rails APIs to keep things simple and stable.
#
# Compared to earlier versions of this generator, there is very limited use of
# stubs and message expectations in this spec.  Stubs are only used when there
# is no simpler way to get a handle on the object needed for the example.
# Message expectations are only used when there is no simpler way to specify
# that an instance is receiving a specific message.

describe ScansController do

  # This should return the minimal set of attributes required to create a valid
  # Scan. As you add validations to Scan, be sure to
  # update the return value of this method accordingly.
  def valid_attributes
    { "url" => "MyText" }
  end

  # This should return the minimal set of values that should be in the session
  # in order to pass any filters (e.g. authentication) defined in
  # ScansController. Be sure to keep this updated too.
  def valid_session
    {}
  end

  describe "GET index" do
    it "assigns all scans as @scans" do
      scan = Scan.create! valid_attributes
      get :index, {}, valid_session
      assigns(:scans).should eq([scan])
    end
  end

  describe "GET show" do
    it "assigns the requested scan as @scan" do
      scan = Scan.create! valid_attributes
      get :show, {:id => scan.to_param}, valid_session
      assigns(:scan).should eq(scan)
    end
  end

  describe "GET new" do
    it "assigns a new scan as @scan" do
      get :new, {}, valid_session
      assigns(:scan).should be_a_new(Scan)
    end
  end

  describe "GET edit" do
    it "assigns the requested scan as @scan" do
      scan = Scan.create! valid_attributes
      get :edit, {:id => scan.to_param}, valid_session
      assigns(:scan).should eq(scan)
    end
  end

  describe "POST create" do
    describe "with valid params" do
      it "creates a new Scan" do
        expect {
          post :create, {:scan => valid_attributes}, valid_session
        }.to change(Scan, :count).by(1)
      end

      it "assigns a newly created scan as @scan" do
        post :create, {:scan => valid_attributes}, valid_session
        assigns(:scan).should be_a(Scan)
        assigns(:scan).should be_persisted
      end

      it "redirects to the created scan" do
        post :create, {:scan => valid_attributes}, valid_session
        response.should redirect_to(Scan.last)
      end
    end

    describe "with invalid params" do
      it "assigns a newly created but unsaved scan as @scan" do
        # Trigger the behavior that occurs when invalid params are submitted
        Scan.any_instance.stub(:save).and_return(false)
        post :create, {:scan => { "url" => "invalid value" }}, valid_session
        assigns(:scan).should be_a_new(Scan)
      end

      it "re-renders the 'new' template" do
        # Trigger the behavior that occurs when invalid params are submitted
        Scan.any_instance.stub(:save).and_return(false)
        post :create, {:scan => { "url" => "invalid value" }}, valid_session
        response.should render_template("new")
      end
    end
  end

  describe "PUT update" do
    describe "with valid params" do
      it "updates the requested scan" do
        scan = Scan.create! valid_attributes
        # Assuming there are no other scans in the database, this
        # specifies that the Scan created on the previous line
        # receives the :update_attributes message with whatever params are
        # submitted in the request.
        Scan.any_instance.should_receive(:update_attributes).with({ "url" => "MyText" })
        put :update, {:id => scan.to_param, :scan => { "url" => "MyText" }}, valid_session
      end

      it "assigns the requested scan as @scan" do
        scan = Scan.create! valid_attributes
        put :update, {:id => scan.to_param, :scan => valid_attributes}, valid_session
        assigns(:scan).should eq(scan)
      end

      it "redirects to the scan" do
        scan = Scan.create! valid_attributes
        put :update, {:id => scan.to_param, :scan => valid_attributes}, valid_session
        response.should redirect_to(scan)
      end
    end

    describe "with invalid params" do
      it "assigns the scan as @scan" do
        scan = Scan.create! valid_attributes
        # Trigger the behavior that occurs when invalid params are submitted
        Scan.any_instance.stub(:save).and_return(false)
        put :update, {:id => scan.to_param, :scan => { "url" => "invalid value" }}, valid_session
        assigns(:scan).should eq(scan)
      end

      it "re-renders the 'edit' template" do
        scan = Scan.create! valid_attributes
        # Trigger the behavior that occurs when invalid params are submitted
        Scan.any_instance.stub(:save).and_return(false)
        put :update, {:id => scan.to_param, :scan => { "url" => "invalid value" }}, valid_session
        response.should render_template("edit")
      end
    end
  end

  describe "DELETE destroy" do
    it "destroys the requested scan" do
      scan = Scan.create! valid_attributes
      expect {
        delete :destroy, {:id => scan.to_param}, valid_session
      }.to change(Scan, :count).by(-1)
    end

    it "redirects to the scans list" do
      scan = Scan.create! valid_attributes
      delete :destroy, {:id => scan.to_param}, valid_session
      response.should redirect_to(scans_url)
    end
  end

end
